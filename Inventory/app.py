from flask import Flask
from flask_cors import CORS
from routes import inventory_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
