import connexion
from .database import configure_database
from .models import db
from .routes import routes, login

import jwt
from connexion.exceptions import OAuthProblem

key = "ApiEndpointsShouldWork"


def verify_bearer_token(token):
    try:
        decoded = jwt.decode(token, key, algorithms=["HS256"])
        print(f"Decoded token: {decoded}")  
        return {"user_id": decoded.get("user_id")}
    except jwt.ExpiredSignatureError:
        raise OAuthProblem(description="Token has expired")
    except jwt.InvalidTokenError:
        raise OAuthProblem(description="Invalid token")


def create_app():
    app = connexion.App(__name__, specification_dir='../swagger', options={"swagger_ui": True})

    # security handler for API
    app.add_api(
        'api.yml',
        options={
            "swagger_ui": True,
            "security_handlers": {"bearerAuth": verify_bearer_token} 
        }
    )

    flask_app = app.app

    configure_database(flask_app)
    flask_app.register_blueprint(routes)

    return flask_app
