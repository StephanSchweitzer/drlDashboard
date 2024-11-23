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

            # Hyperparameter Filters Section
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Hyperparameter Filters"),
                        dbc.CardBody([
                            dbc.Row([
                                # Alpha Input Fields
                                dbc.Col([
                                    html.Label("Alpha", className="fw-bold"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Min"),
                                        dbc.Input(
                                            id="alpha-min",
                                            placeholder="0.0",
                                            type="number",
                                            min=0.0,
                                            max=1.0,
                                            step=0.01,
                                            value=0.0,
                                            size="sm",
                                        ),
                                        dbc.InputGroupText("Max"),
                                        dbc.Input(
                                            id="alpha-max",
                                            placeholder="1.0",
                                            type="number",
                                            min=0.0,
                                            max=1.0,
                                            step=0.01,
                                            value=1.0,
                                            size="sm",
                                        ),
                                    ], className="mb-2", size="sm"),
                                ], md=2, xs=6, className="mb-3"),

                                # Batch Size Input Fields
                                dbc.Col([
                                    html.Label("Batch Size", className="fw-bold"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Min"),
                                        dbc.Input(
                                            id="batch_size-min",
                                            placeholder="1",
                                            type="number",
                                            min=1,
                                            max=1024,
                                            step=1,
                                            value=1,
                                            size="sm",
                                        ),
                                        dbc.InputGroupText("Max"),
                                        dbc.Input(
                                            id="batch_size-max",
                                            placeholder="1024",
                                            type="number",
                                            min=1,
                                            max=1024,
                                            step=1,
                                            value=1024,
                                            size="sm",
                                        ),
                                    ], className="mb-2", size="sm"),
                                ], md=2, xs=6, className="mb-3"),

                                # Gamma Input Fields
                                dbc.Col([
                                    html.Label("Gamma", className="fw-bold"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Min"),
                                        dbc.Input(
                                            id="gamma-min",
                                            placeholder="0.0",
                                            type="number",
                                            min=0.0,
                                            max=1.0,
                                            step=0.01,
                                            value=0.0,
                                            size="sm",
                                        ),
                                        dbc.InputGroupText("Max"),
                                        dbc.Input(
                                            id="gamma-max",
                                            placeholder="1.0",
                                            type="number",
                                            min=0.0,
                                            max=1.0,
                                            step=0.01,
                                            value=1.0,
                                            size="sm",
                                        ),
                                    ], className="mb-2", size="sm"),
                                ], md=2, xs=6, className="mb-3"),

                                # Num Episodes Input Fields
                                dbc.Col([
                                    html.Label("Num Episodes", className="fw-bold"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Min"),
                                        dbc.Input(
                                            id="num_episodes-min",
                                            placeholder="1",
                                            type="number",
                                            min=1,
                                            max=10000,
                                            step=1,
                                            value=1,
                                            size="sm",
                                        ),
                                        dbc.InputGroupText("Max"),
                                        dbc.Input(
                                            id="num_episodes-max",
                                            placeholder="10000",
                                            type="number",
                                            min=1,
                                            max=10000,
                                            step=1,
                                            value=10000,
                                            size="sm",
                                        ),
                                    ], className="mb-2", size="sm"),
                                ], md=2, xs=6, className="mb-3"),

                                # Replay Capacity Input Fields
                                dbc.Col([
                                    html.Label("Replay Capacity", className="fw-bold"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Min"),
                                        dbc.Input(
                                            id="replay_capacity-min",
                                            placeholder="1",
                                            type="number",
                                            min=1,
                                            max=1000000,
                                            step=1000,
                                            value=1,
                                            size="sm",
                                        ),
                                        dbc.InputGroupText("Max"),
                                        dbc.Input(
                                            id="replay_capacity-max",
                                            placeholder="1000000",
                                            type="number",
                                            min=1,
                                            max=1000000,
                                            step=1000,
                                            value=1000000,
                                            size="sm",
                                        ),
                                    ], className="mb-2", size="sm"),
                                ], md=2, xs=6, className="mb-3"),

                                # Start Epsilon Input Fields
                                dbc.Col([
                                    html.Label("Start Epsilon", className="fw-bold"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Min"),
                                        dbc.Input(
                                            id="start_epsilon-min",
                                            placeholder="0.0",
                                            type="number",
                                            min=0.0,
                                            max=1.0,
                                            step=0.01,
                                            value=0.0,
                                            size="sm",
                                        ),
                                        dbc.InputGroupText("Max"),
                                        dbc.Input(
                                            id="start_epsilon-max",
                                            placeholder="1.0",
                                            type="number",
                                            min=0.0,
                                            max=1.0,
                                            step=0.01,
                                            value=1.0,
                                            size="sm",
                                        ),
                                    ], className="mb-2", size="sm"),
                                ], md=2, xs=6, className="mb-3"),
                            ]),
                            dbc.Button(
                                "Apply Filters",
                                id="apply-filters-button",
                                color="primary",
                                className="mt-3"
                            )
                        ])
                    ])
                ], width=12)
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
