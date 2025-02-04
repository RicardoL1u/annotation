from flask import Blueprint, render_template, request, flash, url_for,redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Manager,Annotator, AnnotatorTask,Passage,AnnotatedData
from datetime import timedelta
from . import db
import json
import pytz
from .annotate_data import dataset
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
                login_user(manager,remember=True,duration=timedelta(hours=12))
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
                'message':'Manager not exist, plz connect to admin',
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

@manager.route('/sign_up_annotator',methods=['POST'])
@login_required
def sign_up_annotator():
    if current_user.role != 'manager':
        return {
            'message': 'You have to be a manager to sign up annotator.',
            'code': 0
        }
        
    if Manager.query.get(request.json.get('annotator_id')) or Annotator.query.get(request.json.get('annotator_id')):
        return {
            'message': 'this phone number has been already used!',
            'code': 0
        }


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
        'code':1
    }

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Hong_Kong'))
    return pytz.timezone('Asia/Hong_Kong').normalize(local_dt) # .normalize might be unnecessary
def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

@manager.route('/review_one_data_point', methods=['POST'])
@login_required
def review_one_data_point():
    annotated_filename = request.json.get('annotated_filename')
    data = AnnotatedData.query.filter_by(annotated_filename=annotated_filename).first()
    if not data:
        return {
            'message': 'The annotated data file you requested has not been created yet',
            'code':0
        }

    annotator = Annotator.query.get(data.annotator_id) 
    return {
        'annotated_data':json.load(open('data/'+annotated_filename)),
        'annotator_id': data.annotator_id,
        'annotator_name':annotator.name,
        'create_timestamp':aslocaltimestr(data.create_timestamp),
        'passage_ori_id':data.passage_ori_id,
        'code':1
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

@manager.route('/review_task',methods=["POST"])
@login_required
def review_task():
    if current_user.role!='manager':
        return {
            'message': "Only managers can access this page.",
            'code': 0
        }
    task_id = request.json.get('task_id', None)
    if  not task_id:
        return {
            'message': "Missing required arguments.",
            'code': 0
        }
    task = AnnotatorTask.query.get(task_id)
    annotator = Annotator.query.get(task.annotator_id)
    if not annotator or not task:
        return {
            'message': "Annotator/Task does not exist.",
            'code': 0
        }

    if task.task_status == 0:
        return {
            'message': "Annotator task is not in the finished state.",
            'code': 0
        }
    print(type(annotator.manager_id))
    print(type(current_user.id))
    if task.annotator_id != annotator.id or annotator.manager_id != current_user.id:
        return {
            'message': "You are not allowed to review this task.",
            'code': 0
        }
    task_status = request.json.get('task_status', None)
    if task_status == None:
        return {
            'message': "the last annotated data.",
            'annotated_data':json.load(open('data/'+task.annotated_filename)),
            'passage':dataset[task.passage_id-1], # passage id is the id in database (start from 1)
            'code': 0
        }
    task.task_status = task_status
    # if task_status == 2:
    #     task.annotated_filename = sorted(AnnotatedData.query.filter_by(annotator_id = annotator.id,passage_id=task.passage_id).all(),key =lambda x: x.create_timestamp,reverse=True)[0].annotated_filename
    # elif task_status == 0:
    #     task.annotated_filename = None
    # print(sorted(AnnotatedData.query.filter_by(annotator_id = annotator.id,passage_id=task.passage_id).all(),key =lambda x: x.create_timestamp,reverse=True)[0].annotated_filename)
    db.session.add(task)
    db.session.commit()
    return {
        'message': "task status successfully updated.",
        'code': 1
    }


@manager.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return {
        'mesage': 'You have successfully logged out',
        'code': 1,
    }
