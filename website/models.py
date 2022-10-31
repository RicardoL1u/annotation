from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Manager(db.Model, UserMixin):
    phone = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    token = db.Column(db.String, nullable=False)

class Annotator(db.Model,UserMixin):
    phone = db.Column(db.String, unique=True, primary_key=True)
    name = db.Column(db.String, unique=True)
    # id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    manager_phone = db.Column(db.String, db.ForeignKey('manager.phone'))


class Passage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    passage_id = db.Column(db.String, unique=True, nullable=False)
    done = db.Column(db.Boolean,default=False)

class Annotated_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passage_id = db.Column(db.String,db.ForeignKey('passage.id'))
    create_timestamp = db.Column(db.TIMESTAMP, default=func.now())
    annotator_phone = db.Column(db.String, db.ForeignKey('annotator.phone'))
    annotated_filename = db.Column(db.String,nullable=False)

class Annotator_Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    annotator_phone = db.Column(db.String, db.ForeignKey('annotator.phone'))
    passage_id = db.Column(db.String)
    task_done_number = db.Column(db.Integer, default=0)

    reviewed = db.Column(db.Integer,default=0) 
    # set default to 0 as not reviewed yet
    # when equal to -1 as need re-annotate
    # when equal to 1 as task has been completed and need to assign one final result
    annotated_filename = db.Column(db.String, db.ForeignKey('annotated_data.annotated_filename'))


