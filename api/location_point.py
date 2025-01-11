from flask import request, Response
import json
from models import LocationPoint, Database

# get all location points
def get_location_points():
    points = LocationPoint.query.all()
    response_data = [
        {
            "LocationID": point.LocationID,
            "Latitude": point.Latitude,
            "Longitude": point.Longitude,
            "Location_Description": point.Location_Description
        }
        for point in points
    ]
    return Response(json.dumps(response_data), status=200, mimetype="application/json")


# get a specific location point by ID
def get_location_point_by_id(location_point_id):
    point = LocationPoint.query.get(location_point_id)
    if not point:
        return Response(json.dumps({"error": "Location point not found"}), status=404, mimetype="application/json")
    
    response_data = {
        "LocationID": point.LocationID,
        "Latitude": point.Latitude,
        "Longitude": point.Longitude,
        "Location_Description": point.Location_Description
    }
    return Response(json.dumps(response_data), status=200, mimetype="application/json")


# add a new location point
def create_location_point():
    data = request.get_json()
    if not data or "Latitude" not in data or "Longitude" not in data:
        return Response(json.dumps({"error": "Missing required fields"}), status=400, mimetype="application/json")
    
    new_location_point = LocationPoint(
        Latitude=data["Latitude"],
        Longitude=data["Longitude"],
        Location_Description=data.get("Location_Description")
    )
    Database.session.add(new_location_point)
    Database.session.commit()
    return Response(json.dumps({"message": "Location point added successfully"}), status=202, mimetype="application/json")


# update a location point
def update_location_point(location_point_id):
    data = request.get_json()
    point = LocationPoint.query.get(location_point_id)
    if not point:
        return Response(json.dumps({"error": "Location point not found"}), status=404, mimetype="application/json")
    
    if "Latitude" in data:
        point.Latitude = data["Latitude"]
    if "Longitude" in data:
        point.Longitude = data["Longitude"]
    if "Location_Description" in data:
        point.Location_Description = data["Location_Description"]
    
    Database.session.commit()
    return Response(json.dumps({"message": "Location point updated successfully"}), status=200, mimetype="application/json")


# delete a location point
def delete_location_point(location_point_id):
    point = LocationPoint.query.get(location_point_id)
    if not point:
        return Response(json.dumps({"error": "Location point not found"}), status=404, mimetype="application/json")
    
    Database.session.delete(point)
    Database.session.commit()
    return Response(json.dumps({"message": "Location point deleted successfully"}), status=204, mimetype="application/json")
