import connexion
from .database import configure_database
from .models import db
from .routes import routes, login

def create_app():
    app = connexion.App(__name__, specification_dir='../swagger', options={"swagger_ui": True})
   

    app.add_api('api.yml')  # Enable Swagger UI
    flask_app = app.app

    configure_database(flask_app)

    # Register Blueprints
    flask_app.register_blueprint(routes)
    flask_app.add_url_rule('/login', 'login', login, methods=['POST'])

    return flask_app
