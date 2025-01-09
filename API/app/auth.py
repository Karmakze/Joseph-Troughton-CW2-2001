import jwt
from functools import wraps
from flask import request, jsonify

key = "ApiEndpointsShouldWork"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Expecting "Bearer <token>"
        if not token:
            return jsonify({"message": "Token is missing", "error_code": "401_UNAUTHORIZED"}), 401

        try:
            # Decode the token
            token = token.split()[1]  # Remove "Bearer" prefix
            data = jwt.decode(token, key, algorithms=["HS256"])
            request.user = data  # Pass user info to the request context
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired", "error_code": "401_TOKEN_EXPIRED"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token", "error_code": "401_INVALID_TOKEN"}), 401

        return f(*args, **kwargs)
    return decorated

