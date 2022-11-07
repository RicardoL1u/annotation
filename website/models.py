from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Manager(db.Model, UserMixin):
    # id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    id = db.Column(db.String, primary_key=True) # id is phone
    name = db.Column(db.String, nullable=False, unique=True)
    token = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='manager')
class Annotator(db.Model,UserMixin):
    # id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    token = db.Column(db.String, unique=True)
    manager_id = db.Column(db.String, db.ForeignKey('manager.id'))
    role = db.Column(db.String, default='annotator')    

class Passage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ori_id = db.Column(db.String, unique=True, nullable=False)
    done = db.Column(db.Boolean,default=False)

class AnnotatedData(db.Model):
    __tablename__ = 'annotated_data'
    id = db.Column(db.Integer, primary_key=True)
    passage_ori_id = db.Column(db.String,db.ForeignKey('passage.ori_id'))
    create_timestamp = db.Column(db.TIMESTAMP, default=func.now())
    annotator_id = db.Column(db.String, db.ForeignKey('annotator.id'))
    annotated_filename = db.Column(db.String,nullable=False)

class AnnotatorTask(db.Model):
    __tablename__ = 'annotator_task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    annotator_id = db.Column(db.String, db.ForeignKey('annotator.id'))
    passage_id = db.Column(db.Integer, db.ForeignKey('passage.id'))
    passage_ori_id = db.Column(db.String, db.ForeignKey('passage.ori_id'))
    task_done_number = db.Column(db.Integer, default=0)

    task_status = db.Column(db.Integer,default=0) 
    # set default to 0 as not done yet
    # when equal to 1 as need reviewed new -> if not accepeted -> set back to 0
    # when equal to 2 as already reviewed and accepted

    last_done_timestamp = db.Column(db.TIMESTAMP)
    annotated_filename = db.Column(db.String, db.ForeignKey('annotated_data.annotated_filename'))


