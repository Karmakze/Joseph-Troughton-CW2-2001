from flask import request, jsonify
from .models import db, Trail, Users, City


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
