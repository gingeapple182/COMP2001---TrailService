from flask import jsonify
from models import LocationPoint, Database

def get_location_points():
    points = LocationPoint.query.all()
    return jsonify([{
        "LocationID": point.LocationID,
        "Latitude": point.Latitude,
        "Longitude": point.Longitude,
        "Location_Description": point.Location_Description
    } for point in points])
