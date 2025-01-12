import jwt
from functools import wraps
from flask import request, jsonify

key = "ApiEndpointsShouldWork"

def token_required(f):
    print("Token required")
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  
        print(f"Authorization header received: {token}")
        if not token:
            return jsonify({"message": "Token is missing", "error_code": "401_UNAUTHORIZED"}), 401

        try:
            token = token.split()[1]  # remove bearer
            data = jwt.decode(token, key, algorithms=["HS256"])
            request.user = {"user_id": data["user_id"]}
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired", "error_code": "401_TOKEN_EXPIRED"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token", "error_code": "401_INVALID_TOKEN"}), 401

        return f(*args, **kwargs)
    return decorated


