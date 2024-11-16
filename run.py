from app import app
from app.layout import layout
from app.callbacks import register_callbacks

# Set up the app layout and callbacks
app.layout = layout
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
