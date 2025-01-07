Trails API
Overview
The Trails API is a RESTful API designed to manage trail data for a trails application. It allows users to create, retrieve, update, and delete trail information, as well as authenticate users via a login endpoint. This API is built with Python, Flask, SQLAlchemy, and Connexion, and it uses Docker for containerization.

Features
Trails Management:
Retrieve all trails.
Create new trails.
Update existing trails.
Delete trails.
User Authentication:
Login via an external authentication API.
Issue JWT tokens for session management.
Requirements
Prerequisites
Python 3.10
Docker



Dependencies
All dependencies are listed in requirements.txt. These include:

Flask
Flask-SQLAlchemy
Connexion
PyJWT
Requests
PyODBC
