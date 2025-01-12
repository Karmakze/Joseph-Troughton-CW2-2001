import requests
from flask import request, jsonify

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def authenticate_user():
    credentials = request.json
    response = requests.post(AUTH_API_URL, json=credentials)
    if response.status_code == 200:
        return jsonify({'message': 'Authentication successful'})
    return jsonify({'message': 'Authentication failed'}), 401
