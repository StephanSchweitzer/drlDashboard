from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    # Header with title and refresh button
    dbc.Row([
        dbc.Col([
            html.H1("Model Metrics Visualizer", className="text-center mb-4"),
            dbc.Button(
                "Refresh Model List",
                id="refresh-button",
                color="primary",
                className="mb-4 d-block mx-auto",
                n_clicks=0
            ),
        ], width=12)
    ]),

    # Loading spinner for data loading operations
    dcc.Loading(
        id="loading",
        type="circle",
        children=[
            # Selectors Section
            dbc.Row([
                # Model Folder Selector
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Label("Select Model Folders:", className="fw-bold mb-2"),
                            dcc.Dropdown(
                                id="model-folder-selector",
                                options=[],
                                multi=True,
                                placeholder="Select one or more model folders",
                                className="mb-2"
                            ),
                        ])
                    ])
                ], md=6, className="mb-3"),

                # Metrics File Selector
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Label("Select Metrics Files:", className="fw-bold mb-2"),
                            dcc.Dropdown(
                                id="metrics-file-selector",
                                options=[],
                                multi=True,
                                placeholder="Select one or more metrics files",
                                className="mb-2"
                            ),
                        ])
                    ])
                ], md=6, className="mb-3"),
            ], className="mb-4"),

            # Results Section
            dbc.Row([
                # Hyperparameters Section
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Model Hyperparameters"),
                        dbc.CardBody(
                            html.Div(id="hyperparameters-container")
                        )
                    ], className="mb-4")
                ], width=12),

                # Plots Section
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Performance Metrics"),
                        dbc.CardBody([
                            html.Div(
                                id="plots-container",
                                className="plot-grid"
                            )
                        ])
                    ])
                ], width=12),
            ]),
        ]
    ),

    # Footer with additional information
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P(
                "Select model folders and metrics files to visualize training metrics.",
                className="text-muted text-center"
            )
        ], width=12)
    ], className="mt-4"),

], fluid=True)