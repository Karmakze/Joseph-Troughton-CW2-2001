from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pyodbc

db = SQLAlchemy()

def configure_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"
    ).format(
        username="JTroughton",
        password="QrcL520*",
        server="dist-6-505.uopnet.plymouth.ac.uk",
        database="COMP2001_JTroughton",
        driver="ODBC Driver 17 for SQL Server"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
