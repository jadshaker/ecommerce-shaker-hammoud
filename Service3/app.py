from flask import Flask
from flask_cors import CORS
from routes import reviews_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5002)
