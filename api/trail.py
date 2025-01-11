from flask import request, Response
import json
from models import Trail, LocationPoint, TrailLocationPoint, Database
from authentication import get_user_role

# get all trails
def get_trails():
    trails = Trail.query.all()
    response_data = [
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
    ]
    return Response(json.dumps(response_data), status=200, mimetype="application/json")


# get a specific trail by ID
def get_trail_by_id(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return Response(json.dumps({"error": "Trail not found"}), status=404, mimetype="application/json")
    
    response_data = {
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
    return Response(json.dumps(response_data), status=200, mimetype="application/json")


# get detailed information of a specific trail by ID
def get_trail_details(trail_id):
    # check admin or user
    user_role = get_user_role(request)
    if user_role == None:
        return Response(json.dumps({"error": "You must login to view detailed trail information."}), status=403, mimetype="application/json")

    trail = Trail.query.get(trail_id)
    if not trail:
        return Response(json.dumps({"error": "Trail not found"}), status=404, mimetype="application/json")

    location_points = (
        Database.session.query(LocationPoint)
        .join(TrailLocationPoint, TrailLocationPoint.Location_Point == LocationPoint.LocationID)
        .filter(TrailLocationPoint.TrailID == trail_id)
        .order_by(TrailLocationPoint.Order)
        .all()
    )

    location_points_data = [
        {
            "LocationID": point.LocationID,
            "Latitude": point.Latitude,
            "Longitude": point.Longitude,
            "Location_Description": point.Location_Description
        }
        for point in location_points
    ]

    response_data = {
        "TrailID": trail.TrailID,
        "Trail_Name": trail.Trail_Name,
        "Trail_Summary": trail.Trail_Summary,
        "Trail_Description": trail.Trail_Description,
        "Trail_Difficulty": trail.Trail_Difficulty,
        "Trail_Location": trail.Trail_Location,
        "Trail_Length": trail.Trail_Length,
        "Trail_Elevation_Gain": trail.Trail_Elevation_Gain,
        "Trail_Route_Type": trail.Trail_Route_Type,
        "Trail_OwnerID": trail.Trail_OwnerID,
        "Location_Points": location_points_data
    }

    return Response(json.dumps(response_data), status=200, mimetype="application/json")


# create new trail
def create_trail():
    # check admin or user
    user_role = get_user_role(request)
    if user_role != "Admin":
        return Response(json.dumps({"error": "You do not have permission to create trails."}), status=403, mimetype="application/json")

    data = request.get_json()
    required_fields = ["Trail_Name", "Trail_Summary", "Trail_Difficulty", "Trail_Location", "Trail_Length", "Trail_OwnerID"]
    for field in required_fields:
        if field not in data:
            return Response(json.dumps({"error": f"{field} is required"}), status=400, mimetype="application/json")

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
    
    return Response(json.dumps({"message": "Trail created successfully"}), status=201, mimetype="application/json")


# update existing trail
def update_trail(trail_id):
    # check admin or user
    user_role = get_user_role(request)
    if user_role != "Admin":
        return Response(json.dumps({"error": "You do not have permission to update trails."}), status=403, mimetype="application/json")

    data = request.get_json()
    trail = Trail.query.get(trail_id)
    
    if not trail:
        return Response(json.dumps({"error": "Trail not found"}), status=404, mimetype="application/json")
    
    for key in data:
        if hasattr(trail, key):
            setattr(trail, key, data[key])
    
    Database.session.commit()
    return Response(json.dumps({"message": "Trail updated successfully"}), status=200, mimetype="application/json")


# delete trail
def delete_trail(trail_id):
    # check admin or user
    user_role = get_user_role(request)
    if user_role != "Admin":
        return Response(json.dumps({"error": "You do not have permission to delete trails."}), status=403, mimetype="application/json")

    trail = Trail.query.get(trail_id)
    
    if not trail:
        return Response(json.dumps({"error": "Trail not found"}), status=404, mimetype="application/json")
    
    Database.session.delete(trail)
    Database.session.commit()
    return Response(json.dumps({"message": "Trail deleted successfully"}), status=204, mimetype="application/json")
