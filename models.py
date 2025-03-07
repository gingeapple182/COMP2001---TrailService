from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

Database = SQLAlchemy()

class TrailUser(Database.Model):
    """represents user roles of the application"""
    __tablename__ = "Trail_User"
    __table_args__ = {"schema": "CW2"}

    UserID = Database.Column(Database.Integer, primary_key=True, autoincrement=True)
    Email_Address = Database.Column(Database.String(100), unique=True, nullable=False)
    User_Role = Database.Column(Database.String(50), nullable=False)

class Trail(Database.Model):
    """represents the primary trail data"""
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
    """represents the location point data and order"""
    __tablename__ = "Location_Point"
    __table_args__ = {"schema": "CW2"}
    
    LocationID = Database.Column(Database.Integer, primary_key=True, autoincrement=True)
    Latitude = Database.Column(Database.Float, nullable=False)
    Longitude = Database.Column(Database.Float, nullable=False)
    Location_Description = Database.Column(Database.String(255))

class TrailLocationPoint(Database.Model):
    """link table from Trail to Location_Point"""
    __tablename__ = "Trail_Location_Point"
    __table_args__ = {"schema": "CW2"}

    TrailID = Database.Column(Database.Integer, Database.ForeignKey("CW2.Trail.TrailID"), primary_key=True)
    Location_Point = Database.Column(Database.Integer, Database.ForeignKey("CW2.Location_Point.LocationID"), primary_key=True)
    Order = Database.Column(Database.Integer, nullable=False)

class Tag(Database.Model):
    """Represents Tags and tag types"""
    __tablename__ = "Tag"
    __table_args__ = (
        CheckConstraint("Tag_Type IN ('Trail Info', 'Features', 'Activities')", name="chk_tag_type"),
        {"schema": "CW2"}
    )

    TagID = Database.Column(Database.Integer, primary_key=True, autoincrement=True)
    Tag_Name = Database.Column(Database.String(100), nullable=False)
    Tag_Type = Database.Column(Database.String(20), nullable=False)


class TrailTag(Database.Model):
    """link table from Trail to Tag"""
    __tablename__ = "Trail_Tag"
    __table_args__ = {"schema": "CW2"}

    TrailID = Database.Column(Database.Integer, Database.ForeignKey("CW2.Trail.TrailID"), primary_key=True)
    TagID = Database.Column(Database.Integer, Database.ForeignKey("CW2.Tag.TagID"), primary_key=True)
