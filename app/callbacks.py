from dash import html, dcc, dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import os
import pandas as pd
import logging
from app.utils import get_model_folders, get_metrics_files, load_and_combine_data
from app import app
import json
from dash import callback_context



# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

BASE_DIRECTORY = "../reinforcement_learning_project_IABD/logs"


def check_hyperparameter(param_name, value, min_value, max_value):
    if value is None:
        print(f"problem with {param_name} {value}")
        return True  # Skip if the hyperparameter is missing
    if min_value is not None and value < min_value:
        return False
    if max_value is not None and value > max_value:
        return False
    return True

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
        [
            Input('model-folder-selector', 'value'),
            Input('apply-filters-button', 'n_clicks')
        ],
        [
            State('alpha-min', 'value'),
            State('alpha-max', 'value'),
            State('batch_size-min', 'value'),
            State('batch_size-max', 'value'),
            State('gamma-min', 'value'),
            State('gamma-max', 'value'),
            State('num_episodes-min', 'value'),
            State('num_episodes-max', 'value'),
            State('replay_capacity-min-test', 'value'),
            State('replay_capacity-max', 'value'),
            State('start_epsilon-min', 'value'),
            State('start_epsilon-max', 'value')
        ]
    )
    def update_metrics_file_options(selected_model_folders, n_clicks,
                                    alpha_min, alpha_max,
                                    batch_size_min, batch_size_max,
                                    gamma_min, gamma_max,
                                    num_episodes_min, num_episodes_max,
                                    replay_capacity_min, replay_capacity_max,
                                    start_epsilon_min, start_epsilon_max):
        # Determine which input triggered the callback
        ctx = callback_context
        if not ctx.triggered:
            trigger_id = 'No clicks yet'
        else:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # If no model folders are selected, return an empty list
        if not selected_model_folders:
            return []

        # Initialize an empty set for metrics files
        metrics_files = set()

        logging.info("All input values:")
        logging.info(f"Model folders: {selected_model_folders}")
        logging.info(f"Alpha: {alpha_min} - {alpha_max}")
        logging.info(f"Batch size: {batch_size_min} - {batch_size_max}")
        logging.info(f"Gamma: {gamma_min} - {gamma_max}")
        logging.info(f"Num episodes: {num_episodes_min} - {num_episodes_max}")
        logging.info(f"Replay capacity: {replay_capacity_min} - {replay_capacity_max}")
        logging.info(f"Start epsilon: {start_epsilon_min} - {start_epsilon_max}")

        # Iterate over selected model folders
        for model_folder in selected_model_folders:
            model_path = os.path.join(BASE_DIRECTORY, model_folder)
            metrics_dir = os.path.join(model_path, "metrics")
            hyperparams_dir = os.path.join(model_path, "hyperparameters")
            if os.path.exists(metrics_dir):
                # Get list of metrics files in this model folder
                metrics_files_in_model = [
                    os.path.splitext(f)[0]  # Base name without extension
                    for f in os.listdir(metrics_dir)
                    if f.endswith(".csv")
                ]

                if trigger_id == 'apply-filters-button' and os.path.exists(hyperparams_dir):
                    # Apply hyperparameter filters
                    for base_name in metrics_files_in_model:
                        hyperparams_file = os.path.join(hyperparams_dir, f"{base_name}_hyperparameters.json")
                        if os.path.exists(hyperparams_file):
                            try:
                                with open(hyperparams_file, 'r') as json_file:
                                    hyperparams_data = json.load(json_file)
                                    # Access the nested hyperparameters dictionary
                                    hyperparams = hyperparams_data.get('hyperparameters', {})
                                satisfies_thresholds = True

                                # Check each hyperparameter
                                if not check_hyperparameter('alpha', hyperparams.get('alpha'),
                                                            alpha_min, alpha_max):
                                    satisfies_thresholds = False
                                if not check_hyperparameter('batch_size', hyperparams.get('batch_size'),
                                                            batch_size_min, batch_size_max):
                                    satisfies_thresholds = False
                                if not check_hyperparameter('gamma', hyperparams.get('gamma'),
                                                            gamma_min, gamma_max):
                                    satisfies_thresholds = False
                                if not check_hyperparameter('num_episodes', hyperparams.get('num_episodes'),
                                                            num_episodes_min, num_episodes_max):
                                    satisfies_thresholds = False
                                if not check_hyperparameter('replay_capacity', hyperparams.get('replay_capacity'),
                                                            replay_capacity_min, replay_capacity_max):
                                    satisfies_thresholds = False
                                if not check_hyperparameter('start_epsilon', hyperparams.get('start_epsilon'),
                                                            start_epsilon_min, start_epsilon_max):
                                    satisfies_thresholds = False

                                if satisfies_thresholds:
                                    # Add this metrics file to the set
                                    metrics_files.add(base_name)
                            except Exception as e:
                                print(f"Error reading {hyperparams_file}: {e}")
                        else:
                            print(
                                f"Hyperparameters file not found for metrics file '{base_name}' in model '{model_folder}'")
                else:
                    # Do not apply hyperparameter filters
                    metrics_files.update(metrics_files_in_model)

        # Return sorted list of metrics files
        metrics_files = sorted(list(metrics_files))
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

            metric_columns = [
                col for col in plot_data.columns
                if col not in ['epoch', 'identifier', 'model', 'metrics_file', 'timestamp']
            ]

            plots = []
            for metric in metric_columns:
                fig = px.line(
                    plot_data,
                    x='epoch',  # Set x-axis to epoch
                    y=metric,  # Set y-axis to the metric column
                    color='identifier',  # Different lines for different models/metrics files
                    title=f"{metric} over Epochs",
                    labels={'epoch': 'Epoch', metric: metric}  # Labels for x and y axes
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



    # Callback for collapse functionality
    @app.callback(
        Output("collapse", "is_open"),
        [Input("collapse-button", "n_clicks")],
        [State("collapse", "is_open")],
    )
    def toggle_collapse(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open