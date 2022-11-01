from cmath import log
from flask import Blueprint, render_template, request, flash, url_for,redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Manager,Annotator, AnnotatorTask,Passage,AnnotatedData
from . import db
manager = Blueprint('manager', __name__)

@manager.route('/login', methods=['POST'])
def login():
    print(request)
    if request.method == 'POST':
        print(request.json)
        phone = request.json.get('phone')
        token = request.json.get('token')
        print(phone)
        print(token)
        manager = Manager.query.filter_by(phone=phone).first()
        if manager:
            if check_password_hash(manager.token, token):
                login_user(manager,remember=True)
                return {
                    'message': 'Logged in successfully!',
                    'code': 1,
                }
            else:
                return {
                    'message': 'The token is invalid. Please try again.',
                    'code': 0
                }
        else:
            return {
                'message':'You are not authorized to view this page',
                'code':0
            }

@manager.route('/get_annotators', methods=['POST'])
@login_required
def get_annotators():
    annotators = Annotator.query.filter_by(manager_phone=current_user.phone).all()
    return {
        'message':'Annotators list',
        'annotators': [{
            'phone':x.phone,
            'name':x.name,
            'manager_phone':x.manager_phone,
        } for x in annotators],
        'code':1
    }

@manager.route('/assign_task', methods = ['POST'])
@login_required
def assign_task():
    annotator_phone = request.json.get('annotator_phone')
    annotator = Annotator.query.filter_by(phone=annotator_phone, manager_phone=current_user.phone).first()
    if annotator == None:
        return {
            'message': 'Annotator not found',
            'code': 0
        }

    task_start_idx = request.json.get('task_start_idx')
    task_end_idx = request.json.get('task_end_idx')

    #check if the annotator is already assigned to the task
    suc_cnt = 0
    for idx in range(task_start_idx, task_end_idx+1):
        passage = Passage.query.get(idx)
        if passage:
            # one passage can only be assigned to one annotator once
            if AnnotatorTask.query.filter_by(annotator_phone=annotator_phone, passage_id=idx).first() == None:
                task = AnnotatorTask(
                    annotator_phone=annotator_phone, 
                    passage_id=passage.id,
                    passage_ori_id = passage.ori_id
                )
                db.session.add(task)
                suc_cnt += 1
    db.session.commit()

    return {
        'message': f'Annotator {suc_cnt} task assigned successfully',
        'assigned_task_num': suc_cnt,
        'code': 1
    }

@manager.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return {
        'mesage': 'You have successfully logged out',
        'code': 1,
    }
