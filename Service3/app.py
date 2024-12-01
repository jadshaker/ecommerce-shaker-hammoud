from flask import Flask
from flask_cors import CORS
from routes import sales_bp


def create_app():
    """
    Create and configure the Flask application.

    This function initializes a Flask application, applies Cross-Origin Resource Sharing (CORS) settings,
    and registers the sales blueprint with a URL prefix of "/api/sales".

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(sales_bp, url_prefix="/api/sales")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5003)
