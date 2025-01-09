import connexion
from flask import Flask
from .database import configure_database
from .models import db

def create_app():
    app = connexion.App(__name__, specification_dir='../swagger')
    app.add_api('api.yml')
    flask_app = app.app
    configure_database(flask_app)
    return app
