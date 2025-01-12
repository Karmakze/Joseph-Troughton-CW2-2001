from flask import request, jsonify, Blueprint, redirect
from .models import db, Trail, Users, City
import requests

# auth improts
from .auth import token_required
from sqlalchemy.exc import SQLAlchemyError
import jwt
from datetime import datetime, timedelta
key = "ApiEndpointsShouldWork"

routes = Blueprint('routes', __name__)

# works 50/50 not important enough to fix
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


routes = Blueprint('routes', __name__)

@routes.route('/trails', methods=['POST'])
@token_required
def add_trail():
    data = request.json
    print(f"User ID from token: {request.user['user_id']}") 
    user_id = request.user['user_id']  # get user_id from the token

    if not data or not data.get('Trail_Name'):
        return jsonify({"message": "Invalid input", "error_code": "400_INVALID_INPUT"}), 400

    try:
        new_trail = Trail(
            Trail_Name=data['Trail_Name'],
            Trail_Description=data.get('Trail_Description'),
            Trail_Type=data.get('Trail_Type'),
            Trail_Difficulty=data.get('Trail_Difficulty'),
            Trail_Distance=data.get('Trail_Distance'),
            Trail_Elevation_Gain=data.get('Trail_Elevation_Gain'),
            Trail_Length=data.get('Trail_Length'),
            Trail_Rating=data.get('Trail_Rating'),
            Trail_City_ID=data['Trail_City_ID'],
            Trail_Creator=user_id
        )
        db.session.add(new_trail)
        db.session.commit()

        return jsonify({"message": "Trail added successfully", "Trail_ID": new_trail.Trail_ID}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Error creating trail", "error_code": "500_DATABASE_ERROR"}), 500

@routes.route('/trails/<int:trail_id>', methods=['PUT'])
@token_required
def update_trail(trail_id):
    trail = Trail.query.get(trail_id)
    user_id = request.user['user_id']  # get user_id from the token

    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    if trail.Trail_Creator != user_id:
        return jsonify({"message": "Unauthorized access", "error_code": "403_FORBIDDEN"}), 403

    data = request.json
    try:
        for key, value in data.items():
            setattr(trail, key, value)
        db.session.commit()
        return jsonify({"message": "Trail updated successfully"})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Error updating trail", "error_code": "500_DATABASE_ERROR"}), 500


@routes.route('/trails/<int:trail_id>', methods=['DELETE'])
@token_required
def delete_trail(trail_id):
    trail = Trail.query.get(trail_id)
    user_id = request.user['user_id']  # get user_id from the token

    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    if trail.Trail_Creator != user_id:
        return jsonify({"message": "Unauthorized access", "error_code": "403_FORBIDDEN"}), 403

    try:
        db.session.delete(trail)
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully"})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting trail", "error_code": "500_DATABASE_ERROR"}), 500

def login():
    auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
    credentials = request.json

    print("Incoming request JSON:", credentials)

    if not credentials or not credentials.get('email') or not credentials.get('password'):
        return jsonify({"message": "Invalid input", "error_code": "400_INVALID_INPUT"}), 400

    response = requests.post(auth_url, json=credentials, headers={"Content-Type": "application/json"})
    print("Auth API response status:", response.status_code)
    print("Auth API response body:", response.text)

    if response.status_code == 200:
        result = response.json()
        if result == ["Verified", "True"]:
            # get data via email on DB
            user = Users.query.filter_by(User_Email=credentials['email']).first()
            if not user:
                return jsonify({"message": "User not found in the database", "error_code": "404_USER_NOT_FOUND"}), 404

            token = jwt.encode(
                {
                    "user_id": user.User_ID,
                    "username": user.User_Name,
                    "exp": datetime.utcnow() + timedelta(hours=1)  # set expiree 
                },
                key,
                algorithm="HS256"
            )

            return jsonify({"message": "Login successful", "token": token}), 200

        elif result == ["Verified", "False"]:
            return jsonify({"message": "Invalid credentials", "error_code": "401_UNAUTHORIZED"}), 401

    return jsonify({"message": "Authentication server error", "error_code": "500_AUTH_SERVER_ERROR"}), 500



