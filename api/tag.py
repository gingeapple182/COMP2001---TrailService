from flask import request, Response
import json
from models import Tag, Database
from authentication import get_user_role

# Get all tags
def get_tags():
    # check admin or user
    user_role = get_user_role(request)
    if user_role != "Admin":
        return Response(json.dumps({"error": "You do not have permission to view tags."}), status=403, mimetype="application/json")

    tags = Tag.query.all()
    response_data = [
        {
            "TagID": tag.TagID,
            "Tag_Name": tag.TagName
        }
        for tag in tags
    ]
    return Response(json.dumps(response_data), status=200, mimetype="application/json")


# Add a new tag
def create_tag():
    # check admin or user
    user_role = get_user_role(request)
    if user_role != "Admin":
        return Response(json.dumps({"error": "You do not have permission to add tags."}), status=403, mimetype="application/json")

    data = request.get_json()
    if not data or "Tag_Name" not in data or "Tag_Type" not in data:
        return Response(json.dumps({"error": "Missing required fields"}), status=400, mimetype="application/json")
    
    valid_types = ["Trail_Info", "Features", "Activities"]
    if data["Tag_Type"] not in valid_types:
        return Response(json.dumps({"error": "Invalid Tag_Type, Must be 'Trail Info', 'Features' or 'Activities'" }), status=400, mimetype="application/json")

    new_tag = Tag(TagName=data["Tag_Name"], Tag_Type=data["Tag_Type"])
    Database.session.add(new_tag)
    Database.session.commit()
    return Response(json.dumps({"message": "Tag added successfully"}), status=202, mimetype="application/json")


# Update an existing tag
def update_tag(tag_id):
    # check admin or user
    user_role = get_user_role(request)
    if user_role != "Admin":
        return Response(json.dumps({"error": "You do not have permission to update tags."}), status=403, mimetype="application/json")

    data = request.get_json()
    tag = Tag.query.get(tag_id)
    if not tag:
        return Response(json.dumps({"error": "Tag not found"}), status=404, mimetype="application/json")
    
    if "Tag_Name" in data:
        tag.TagName = data["Tag_Name"]
    
    Database.session.commit()
    return Response(json.dumps({"message": "Tag updated successfully"}), status=200, mimetype="application/json")


# Delete a tag
def delete_tag(tag_id):
    # check admin or user
    user_role = get_user_role(request)
    if user_role != "Admin":
        return Response(json.dumps({"error": "You do not have permission to delete tags."}), status=403, mimetype="application/json")

    tag = Tag.query.get(tag_id)
    if not tag:
        return Response(json.dumps({"error": "Tag not found"}), status=404, mimetype="application/json")
    
    Database.session.delete(tag)
    Database.session.commit()
    return Response(json.dumps({"message": "Tag deleted successfully"}), status=204, mimetype="application/json")
