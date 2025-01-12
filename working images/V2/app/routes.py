from flask import request, jsonify, Blueprint, redirect
from .models import db, Trail, Users, City
import requests

# auth improts
from .auth import token_required
import jwt
from datetime import datetime, timedelta
key = "ApiEndpointsShouldWork"

routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET'])
def redirect_to_ui():
    return redirect('/ui/')


@routes.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({"message": f"Welcome {request.user['username']}! You have access to this resource."})

@routes.route('/unprotected', methods=['GET'])
def unprotected():
    return jsonify({"message": "This is a public endpoint."})


# GET all trails
def get_trails():
    trails = Trail.query.all()
    result = [
        {
            "Trail_ID": trail.Trail_ID,
            "Trail_Name": trail.Trail_Name,
            "Trail_Description": trail.Trail_Description,
            "Trail_Type": trail.Trail_Type,
            "Trail_Difficulty": trail.Trail_Difficulty,
            "Trail_Distance": float(trail.Trail_Distance) if trail.Trail_Distance else None,
            "Trail_Elevation_Gain": float(trail.Trail_Elevation_Gain) if trail.Trail_Elevation_Gain else None,
            "Trail_Length": trail.Trail_Length,
            "Trail_Rating": float(trail.Trail_Rating) if trail.Trail_Rating else None,
            "Trail_City_ID": trail.Trail_City_ID,
            "Trail_Creator": trail.Trail_Creator
        }
        for trail in trails
    ]
    return jsonify(result)


# POST a new trail
def add_trail():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid input format", "error_code": "400_INVALID_INPUT"}), 400
    # Check for duplicate trail names (example)
    if Trail.query.filter_by(Trail_Name=data.get('Trail_Name')).first():
        return jsonify({"message": "Trail name already exists", "error_code": "409_CONFLICT"}), 409
    # Proceed with adding trail
    trail = Trail(**data)
    db.session.add(trail)
    db.session.commit()
    return jsonify({"message": "Trail added successfully", "Trail_ID": trail.Trail_ID}), 201



# PUT (update) a trail
def update_trail(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    data = request.json
    for key, value in data.items():
        setattr(trail, key, value)
    db.session.commit()
    return jsonify({"message": "Trail updated successfully"})


# DELETE a trail
def delete_trail(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    db.session.delete(trail)
    db.session.commit()
    return jsonify({"message": "Trail deleted successfully"})

def login():
    auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
    credentials = request.json

    # Log incoming request
    print("Incoming request JSON:", credentials)

    if not credentials or not credentials.get('email') or not credentials.get('password'):
        return jsonify({"message": "Invalid input", "error_code": "400_INVALID_INPUT"}), 400

    # Do not transform credentials
    print("Credentials for Auth API:", credentials)

    response = requests.post(auth_url, json=credentials, headers={"Content-Type": "application/json"})
    print("Auth API response status:", response.status_code)
    print("Auth API response body:", response.text)

    if response.status_code == 200:
        result = response.json()
        if result == ["Verified", "True"]:
            # Create a JWT token
            token = jwt.encode(
                {
                    "username": credentials['email'],  # Use email for token creation
                    "exp": datetime.utcnow() + timedelta(hours=1)
                },
                key,
                algorithm="HS256"
            )
            return jsonify({"message": "Login successful", "token": token}), 200
        elif result == ["Verified", "False"]:
            return jsonify({"message": "Invalid credentials", "error_code": "401_UNAUTHORIZED"}), 401

    return jsonify({"message": "Authentication server error", "error_code": "500_AUTH_SERVER_ERROR"}), 500


