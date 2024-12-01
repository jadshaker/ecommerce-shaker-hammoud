from flask import Flask, jsonify
from flask_cors import CORS
from routes import customer_bp


def create_app():
    """
    Create and configure the Flask application.

    This function sets up the Flask application, enables Cross-Origin Resource Sharing (CORS),
    and registers the customer blueprint with a specified URL prefix.

    Returns:
        Flask: The configured Flask application instance.
    """
    # Create Flask app
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Register customer blueprint
    app.register_blueprint(customer_bp, url_prefix="/api/customers")

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
