import connexion
from flask import Flask
from api.user import get_users
from api.trail import get_trails
from api.location_point import get_location_points
from authentication import User_Authentication#, Bearer_Token_Verification
from models import Database, TrailUser

# Database configuration
Database_Configuration = {
    "username": "OCole",
    "password": "LjeP643*",
    "server": "dist-6-505.uopnet.plymouth.ac.uk",
    "database": "COMP2001_OCole",
    "driver": "ODBC+Driver+17+for+SQL+Server"
}

# Connection string
Connexion_String = (
    f"mssql+pyodbc://{Database_Configuration['username']}:{Database_Configuration['password']}@"
    f"{Database_Configuration['server']}/{Database_Configuration['database']}?"
    f"driver={Database_Configuration['driver']}&TrustServerCertificate=yes&Encrypt=yes"
)

# Initialize Connexion app
Connexion_App = connexion.App(__name__, specification_dir="./")
Flask_App = Connexion_App.app

# Configure SQLAlchemy
Flask_App.config['SQLALCHEMY_DATABASE_URI'] = Connexion_String
Flask_App.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Flask_App.add_url_rule("/login", view_func=User_Authentication, methods=["POST"])

# Initialize database
Database.init_app(Flask_App)

# Add API with Swagger
#Connexion_App.add_api("swagger.yml", options={"swagger_ui": True}, arguments={"bearerInfoFunc": Bearer_Token_Verification})

# from authentication import User_Authentication, Bearer_Token_Verification

# Temporarily remove Bearer_Token_Verification from add_api
Connexion_App.add_api("swagger.yml", options={"swagger_ui": True})  # Removed arguments={"bearerInfoFunc": Bearer_Token_Verification}

if __name__ == "__main__":
    with Flask_App.app_context():
        Database.create_all()  # Create tables if they don't exist
    Connexion_App.run(use_reloader=True)
