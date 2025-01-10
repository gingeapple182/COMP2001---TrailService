import connexion
from flask import Flask
from api.user import get_users
from api.trail import get_trails, get_trail_by_id, create_trail, update_trail, delete_trail
from api.location_point import get_location_points
from authentication import User_Authentication
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

# swagger functions
Flask_App.add_url_rule("/login", view_func=User_Authentication, methods=["POST"])

# trail CRUD functions
Flask_App.add_url_rule("/trails", view_func=create_trail, methods=["POST"])
Flask_App.add_url_rule("/trails", view_func=get_trails, methods=["GET"])
Flask_App.add_url_rule("/trails/<int:trail_id>", view_func=get_trail_by_id, methods=["GET"])
Flask_App.add_url_rule("/trails/<int:trail_id>", view_func=update_trail, methods=["PUT"])
Flask_App.add_url_rule("/trails/<int:trail_id>", view_func=delete_trail, methods=["DELETE"])

# Initialize database
Database.init_app(Flask_App)

Connexion_App.add_api("swagger.yml", options={"swagger_ui": True})  # Removed arguments={"bearerInfoFunc": Bearer_Token_Verification}

if __name__ == "__main__":
    with Flask_App.app_context():
        Database.create_all()  # Create tables if they don't exist
    Connexion_App.run(use_reloader=True)
