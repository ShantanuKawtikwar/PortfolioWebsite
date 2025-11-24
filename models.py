from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    date = db.Column(db.String(50))

class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    issuer = db.Column(db.String(150))
    date = db.Column(db.String(50))

class Timeline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(50))
    title = db.Column(db.String(200))
    organization = db.Column(db.String(150))
    details = db.Column(db.Text)
