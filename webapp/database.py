from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key
    username = db.Column(db.String(50), unique=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    birthday = db.Column(db.Integer)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(80))
