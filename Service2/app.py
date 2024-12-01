from flask import Flask
from flask_cors import CORS
from routes import inventory_bp


def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask application, applies Cross-Origin Resource Sharing (CORS) settings,
    and registers the inventory blueprint with a specified URL prefix.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
