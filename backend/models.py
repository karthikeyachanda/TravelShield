from backend.database import db

# User table model
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(100), nullable=False)

    
class Incident(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    description = db.Column(db.String(200))