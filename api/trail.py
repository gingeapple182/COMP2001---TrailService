from flask import request, jsonify
from models import Trail, Database

# get all trails
def get_trails():
    trails = Trail.query.all()
    return jsonify([
        {
            "TrailID": trail.TrailID,
            "Trail_Name": trail.Trail_Name,
            "Trail_Summary": trail.Trail_Summary,
            "Trail_Description": trail.Trail_Description,
            "Trail_Difficulty": trail.Trail_Difficulty,
            "Trail_Location": trail.Trail_Location,
            "Trail_Length": trail.Trail_Length,
            "Trail_Elevation_Gain": trail.Trail_Elevation_Gain,
            "Trail_Route_Type": trail.Trail_Route_Type,
            "Trail_OwnerID": trail.Trail_OwnerID
        }
        for trail in trails
    ]), 200

# get a specific trail by ID
def get_trail_by_id(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"error": "Trail not found"}), 404
    
    return jsonify({
        "TrailID": trail.TrailID,
        "Trail_Name": trail.Trail_Name,
        "Trail_Summary": trail.Trail_Summary,
        "Trail_Description": trail.Trail_Description,
        "Trail_Difficulty": trail.Trail_Difficulty,
        "Trail_Location": trail.Trail_Location,
        "Trail_Length": trail.Trail_Length,
        "Trail_Elevation_Gain": trail.Trail_Elevation_Gain,
        "Trail_Route_Type": trail.Trail_Route_Type,
        "Trail_OwnerID": trail.Trail_OwnerID
    }), 200

# create new trail
def create_trail():
    data = request.get_json()
    required_fields = ["Trail_Name", "Trail_Summary", "Trail_Difficulty", "Trail_Location", "Trail_Length", "Trail_OwnerID"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    new_trail = Trail(
        Trail_Name=data["Trail_Name"],
        Trail_Summary=data["Trail_Summary"],
        Trail_Description=data.get("Trail_Description"),
        Trail_Difficulty=data["Trail_Difficulty"],
        Trail_Location=data["Trail_Location"],
        Trail_Length=data["Trail_Length"],
        Trail_Elevation_Gain=data.get("Trail_Elevation_Gain", 0),
        Trail_Route_Type=data.get("Trail_Route_Type", "Circular"),
        Trail_OwnerID=data["Trail_OwnerID"]
    )
    
    Database.session.add(new_trail)
    Database.session.commit()
    
    return jsonify({"message": "Trail created successfully"}), 201

# update existing trail
def update_trail(trail_id):
    data = request.get_json()
    trail = Trail.query.get(trail_id)
    
    if not trail:
        return jsonify({"error": "Trail not found"}), 404
    
    for key in data:
        if hasattr(trail, key):
            setattr(trail, key, data[key])
    
    Database.session.commit()
    return jsonify({"message": "Trail updated successfully"}), 200

# delete trail
def delete_trail(trail_id):
    trail = Trail.query.get(trail_id)
    
    if not trail:
        return jsonify({"error": "Trail not found"}), 404
    
    Database.session.delete(trail)
    Database.session.commit()
    return jsonify({"message": "Trail deleted successfully"}), 204
