from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))