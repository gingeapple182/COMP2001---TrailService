from flask import jsonify
from models import LocationPoint, Database

# get all location points
def get_location_points():
    points = LocationPoint.query.all()
    return jsonify([{
        "LocationID": point.LocationID,
        "Latitude": point.Latitude,
        "Longitude": point.Longitude,
        "Location_Description": point.Location_Description
    } for point in points])

# get a specific location point by ID
def get_location_point_by_id(location_point_id):
    point = LocationPoint.query.get(location_point_id)
    if not point:
        return jsonify({"error": "Location point not found"}), 404
    
    return jsonify({
        "Location_Point": point.Location_Point,
        "Latitude": point.Latitude,
        "Longitude": point.Longitude,
        "Location_Description": point.Location_Description
    }), 200

# add a new location point
def create_location_point():
    data = request.get_json()
    if not data or "Latitude" not in data or "Longitude" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    new_location_point = LocationPoint(
        Latitude=data["Latitude"],
        Longitude=data["Longitude"],
        Location_Description=data.get("Location_Description")
    )
    Database.session.add(new_location_point)
    Database.session.commit()
    return jsonify({"message": "Location point added successfully"}), 202

# update a location point
def update_location_point(location_point_id):
    data = request.get_json()
    point = LocationPoint.query.get(location_point_id)
    if not point:
        return jsonify({"error": "Location point not found"}), 404
    
    if "Latitude" in data:
        point.Latitude = data["Latitude"]
    if "Longitude" in data:
        point.Longitude = data["Longitude"]
    if "Location_Description" in data:
        point.Location_Description = data["Location_Description"]
    
    Database.session.commit()
    return jsonify({"message": "Location point updated successfully"}), 200


# delete a location point
def delete_location_point(location_point_id):
    point = LocationPoint.query.get(location_point_id)
    if not point:
        return jsonify({"error": "Location point not found"}), 404
    
    Database.session.delete(point)
    Database.session.commit()
    return jsonify({"message": "Location point deleted successfully"}), 204
