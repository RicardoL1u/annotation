from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class Annotator(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    annotator_name = db.Column(db.String(30), unique=True)
    token = db.Column(db.String(30), unique=True)
