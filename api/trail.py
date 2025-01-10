from flask import jsonify
from models import Trail, Database

def get_trails():
    trails = Trail.query.all()
    return jsonify([{
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
    } for trail in trails])
