from flask import Flask
from flask_cors import CORS
from routes import sales_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(sales_bp, url_prefix="/api/sales")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5003)
