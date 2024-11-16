from dash import Dash

# Initialize Dash app
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Expose the Flask server for deployment
