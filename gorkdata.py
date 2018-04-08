from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from uuid import uuid4

db = SQLAlchemy()

def gen_uuid():
    return str(uuid4())


class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    def coords() -> tuple:
        return (lat, lon)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
