from dash import html, dcc, dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import os
import pandas as pd
import logging
from app.utils import get_model_folders, get_metrics_files, load_and_combine_data
from app import app

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

BASE_DIRECTORY = "../reinforcement_learning_project_IABD/logs"


def register_callbacks(app):
    # First callback: Update model folder options
    @app.callback(
        Output('model-folder-selector', 'options'),
        [Input('refresh-button', 'n_clicks')]  # Changed to use refresh button instead
    )
    def update_model_folder_options(n_clicks):
        models = get_model_folders(BASE_DIRECTORY)
        return [{'label': model, 'value': model} for model in models]




    @app.callback(
        Output('metrics-file-selector', 'options'),
        [Input('model-folder-selector', 'value')],
        prevent_initial_call=True
    )
    def update_metrics_file_options(selected_model_folders):
        if not selected_model_folders:
            return []
        metrics_files = get_metrics_files(selected_model_folders, BASE_DIRECTORY)
        return [{'label': f, 'value': f} for f in metrics_files]




    @app.callback(
        [
            Output('hyperparameters-container', 'children'),
            Output('plots-container', 'children')
        ],
        [
            Input('model-folder-selector', 'value'),
            Input('metrics-file-selector', 'value')
        ],
        prevent_initial_call=True
    )
    def update_output(selected_models, selected_metrics_files):
        if not selected_models or not selected_metrics_files:
            return html.Div(), html.Div("Please select model folders and metrics files.")

        try:
            data_list = load_and_combine_data(selected_models, selected_metrics_files, BASE_DIRECTORY)

            if not data_list:
                return html.Div(), html.Div("No data available for selected models and metrics files.")

            # Process hyperparameters
            hyperparams_components = []
            all_metrics_df = []

            for data in data_list:
                metrics_df = data['metrics']
                hyperparams_df = data['hyperparams']
                model = data['model']
                metrics_file = data['metrics_file']

                # Create hyperparameters display
                hyperparams_html = html.Div([
                    html.H3(f"Hyperparameters for {model} - {metrics_file}"),
                    html.Ul([
                        html.Li(f"{k}: {v}")
                        for k, v in hyperparams_df.iloc[0].items()
                    ])
                ], className="mb-4")
                hyperparams_components.append(hyperparams_html)

                # Prepare metrics data
                metrics_df['identifier'] = f"{model} - {metrics_file}"
                all_metrics_df.append(metrics_df)

            # Combine all metrics data
            plot_data = pd.concat(all_metrics_df, ignore_index=True)
            plot_data['timestamp'] = pd.to_datetime(plot_data['timestamp'], errors='coerce')

            # Generate plots
            metric_columns = [
                col for col in plot_data.columns
                if col not in ['timestamp', 'model', 'metrics_file', 'identifier']
            ]

            plots = []
            for metric in metric_columns:
                fig = px.line(
                    plot_data,
                    x='timestamp',
                    y=metric,
                    color='identifier',
                    title=f"{metric} over Time",
                    labels={'timestamp': 'Timestamp', metric: metric}
                )
                # Make the figure smaller to fit two columns
                fig.update_layout(
                    height=400,  # Adjust this value as needed
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                plots.append(
                    html.Div(
                        dcc.Graph(figure=fig),
                        className="plot-item"
                    )
                )

            return html.Div(hyperparams_components), html.Div(plots, className="plot-grid")

        except Exception as e:
            logging.error(f"Error in update_output: {str(e)}")
            return html.Div(f"Error: {str(e)}"), html.Div()