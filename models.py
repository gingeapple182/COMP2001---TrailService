from flask_sqlalchemy import SQLAlchemy

Database = SQLAlchemy()

class TrailUser(Database.Model):
    __tablename__ = "Trail_User"
    __table_args__ = {"schema": "CW2"}

    UserID = Database.Column(Database.Integer, primary_key=True, autoincrement=True)
    Email_Address = Database.Column(Database.String(100), unique=True, nullable=False)
    User_Role = Database.Column(Database.String(50), nullable=False)

class Trail(Database.Model):
    __tablename__ = "Trail"
    __table_args__ = {"schema": "CW2"}
    
    TrailID = Database.Column(Database.Integer, primary_key=True, autoincrement=True)
    Trail_Name = Database.Column(Database.String(100), nullable=False)
    Trail_Summary = Database.Column(Database.String(255), nullable=False)
    Trail_Description = Database.Column(Database.Text)
    Trail_Difficulty = Database.Column(Database.String(10), nullable=False)
    Trail_Location = Database.Column(Database.String(100), nullable=False)
    Trail_Length = Database.Column(Database.Float, nullable=False)
    Trail_Elevation_Gain = Database.Column(Database.Float, nullable=False)
    Trail_Route_Type = Database.Column(Database.String(50), nullable=False)
    Trail_OwnerID = Database.Column(
        Database.Integer, 
        Database.ForeignKey("CW2.Trail_User.UserID"), 
        nullable=False)

class LocationPoint(Database.Model):
    __tablename__ = "Location_Point"
    __table_args__ = {"schema": "CW2"}
    
    LocationID = Database.Column(Database.Integer, primary_key=True, autoincrement=True)
    Latitude = Database.Column(Database.Float, nullable=False)
    Longitude = Database.Column(Database.Float, nullable=False)
    Location_Description = Database.Column(Database.String(255))
