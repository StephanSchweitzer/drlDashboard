from dash import Input, Output, State, ctx
import pandas as pd
import plotly.express as px
import os
from app.utils import load_csv_files, process_csv
from dash import html


def register_callbacks(app):
    @app.callback(
        Output("csv-selector", "options"),
        Input("csv-selector", "value"),
        prevent_initial_call=False
    )
    def update_dropdown(_):
        csv_files = load_csv_files("data")
        return [{"label": file, "value": file} for file in csv_files]

    @app.callback(
        [Output("data-plot", "figure"), Output("table-container", "children")],
        Input("csv-selector", "value"),
    )
    def display_csv(csv_file):
        if not csv_file:
            return {}, "Please select a CSV file"

        df = process_csv(os.path.join("data", csv_file))

        # Example: Scatter plot of the first two columns
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title="Scatter Plot")

        # Example: Render table
        table = html.Table(
            [html.Tr([html.Th(col) for col in df.columns])] +
            [html.Tr([html.Td(str(df.iloc[i, col])) for col in range(len(df.columns))]) for i in
             range(min(10, len(df)))]
        )

        return fig, table
