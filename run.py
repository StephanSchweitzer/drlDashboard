from app import app
from app.layout import layout  # Import your layout
from app.callbacks import register_callbacks  # Import callback registration

# Assign the layout
app.layout = layout

# Register callbacks
register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
