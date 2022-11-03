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
        id = request.json.get('id')
        token = request.json.get('token')
        print(id)
        print(token)
        manager = Manager.query.filter_by(id=id).first()
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
    annotators = Annotator.query.filter_by(manager_id=current_user.id).all()
    return {
        'message':'Annotators list',
        'annotators': [{
            'id':x.id,
            'name':x.name,
            'manager_id':x.manager_id,
        } for x in annotators],
        'code':1
    }

@manager.route('/assign_task', methods = ['POST'])
@login_required
def assign_task():
    annotator_id = request.json.get('annotator_id')
    annotator = Annotator.query.filter_by(id=annotator_id, manager_id=current_user.id).first()
    if annotator == None:
        return {
            'message': 'Annotator not found',
            'code': 0
        }

    passage_start_idx = request.json.get('passage_start_idx')
    passage_end_idx = request.json.get('passage_end_idx')

    #check if the annotator is already assigned to the task
    suc_cnt = 0
    for idx in range(passage_start_idx, passage_end_idx+1):
        passage = Passage.query.get(idx)
        if passage:
            # one passage can only be assigned to one annotator once
            if AnnotatorTask.query.filter_by(annotator_id=annotator_id, passage_id=idx).first() == None:
                task = AnnotatorTask(
                    annotator_id=annotator_id, 
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

@manager.route('sign_up_annotator',methods=['POST'])
@login_required
def sign_up_annotator():
    new_annotator = Annotator(
        id=request.json.get('annotator_id'),
        name = request.json.get('annotator_name'),
        token = generate_password_hash(request.json.get('annotator_token'),method='sha256'),
        manager_id = current_user.id,
        role = 'annotator'
    )
    db.session.add(new_annotator)
    db.session.commit()
    return {
        'message': f'Annotator has been successfully sign up',
        'code':0
    }

@manager.route('/get_task_list',methods=["POST"])
@login_required
def get_task_list():
    if current_user.role != 'manager':
        return {
            'message': "Only managers can access this page.",
            'code': 0
        }
    annotators = Annotator.query.filter_by(manager_id=current_user.id).all()
    tasks = []
    for annotator in annotators:
        tasks.extend([
            {
                'task_id':task.id,
                'annotator_id':task.annotator_id,
                'passage_id':task.passage_id,
                'passage_ori_id':task.passage_ori_id,
                'task_done_number':task.task_done_number,
                'task_status':task.task_status,
                'last_done_timestamp':task.last_done_timestamp,
                'annotated_filename':task.annotated_filename,
            }for task in AnnotatorTask.query.filter_by(annotator_id=annotator.id).all()
            ]
        )
    return {
        'messages':'here is the task list of this manager',
        'task_list':tasks,
        'code':1
    }

@manager.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return {
        'mesage': 'You have successfully logged out',
        'code': 1,
    }
