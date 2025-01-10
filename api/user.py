from flask import jsonify
from models import TrailUser, Database

def get_users():
    users = TrailUser.query.all()
    return jsonify([{
        "UserID": user.UserID,
        "Email_Address": user.Email_Address,
        "User_Role": user.User_Role
    } for user in users])
