from flask import Flask, jsonify
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

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy"}), 200
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
