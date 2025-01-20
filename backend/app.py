from flask import Flask
from database import setup_db
from resources import init_api
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize database
    db = setup_db(app)

    # Initialize API
    init_api(app)

    return app


# WSGI application
app = create_app()
CORS(app)
import os
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == "__main__":
    app.run(debug=True)
