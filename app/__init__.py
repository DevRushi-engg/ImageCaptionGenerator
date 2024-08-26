print("Initializing Flask app...")

from flask import Flask

def create_app():
    print("Creating Flask app...")
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello, World!'

    return app
