from flask import Flask, jsonify
from flask_cors import CORS
from routes import reviews_bp


def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask application, enables Cross-Origin Resource Sharing (CORS),
    and registers the reviews blueprint with a URL prefix of "/api/reviews".

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(reviews_bp, url_prefix="/api/reviews")

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy"}), 200
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5002)
