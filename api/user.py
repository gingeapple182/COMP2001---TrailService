from flask import Response
import json
from models import TrailUser, Database

def get_users():
    users = TrailUser.query.all()
    response_data = [ 
        {       
            "UserID": user.UserID,
            "Email_Address": user.Email_Address,
            "User_Role": user.User_Role
        }
        for user in users
    ]
    return Response(json.dumps(response_data), status=200, mimetype="application/json")
