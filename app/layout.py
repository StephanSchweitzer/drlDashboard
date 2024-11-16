from dash import html, dcc

layout = html.Div([
    html.H1("CSV Visualizer"),
    dcc.Dropdown(id="csv-selector", placeholder="Select a CSV file"),
    dcc.Graph(id="data-plot"),
    html.Div(id="table-container"),
])
