from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    tech_stack = db.Column(db.String(200)) # Added for badges
    link = db.Column(db.String(300))
    image = db.Column(db.String(300))

class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    issuer = db.Column(db.String(200))
    date = db.Column(db.String(50))
    image = db.Column(db.String(300))

class Timeline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(20)) # Changed month to year/date for better sorting
    title = db.Column(db.String(200))
    organization = db.Column(db.String(200))
    details = db.Column(db.Text)
