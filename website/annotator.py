from flask import Blueprint, request

from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import Annotator,AnnotatorTask,Passage
from .annotate_data import dataset
from datetime import timedelta
annotator = Blueprint('annotator', __name__)
# dataset = json.load(open('website/company_data.json'))


@annotator.route('/login', methods=['POST'])
def login():
    print(request)
    if request.method == 'POST':
        print(request.json)
        id = request.json.get('id')
        token = request.json.get('token')
        print(id)
        print(token)
        annotator = Annotator.query.filter_by(id=id).first()
        if annotator:
            if check_password_hash(annotator.token, token):
                login_user(annotator,remember=True,duration=timedelta(hours=12))
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
                'message':'Annotator not exist, plz connect to your manager',
                'code':0
            }

@annotator.route('/get_task_list',methods=['POST'])
@login_required
def get_task_list():
    if current_user.role != 'annotator':
        return {
            'message': "Only annotators can access this page.",
            'code': 0
        }
    tasks = AnnotatorTask.query.filter_by(annotator_id = current_user.id).all()
    return {
        'message': 'here is the task list',
        'task_list':[
            {
                'passage_id':task.passage_id,
                'passage_title': dataset[task.passage_id]['title'],
                'passage_topic_entity':dataset[task.passage_id]['topic_entity']['en']['label'],
                'task_done_number':task.task_done_number
            } for task in tasks
        ],
        'code':0
    }


# @annotator.route('/sign_up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         annotator_name = request.form.get('annotator_name')
#         token = request.form.get('token')

#         annotator = Annotator.query.filter_by(annotator_name=annotator_name).first()
#         print('what')
#         if annotator:
#             flash('Annotator already exists.', category='error')
#         else:
#             new_annotator = Annotator(annotator_name=annotator_name, token=generate_password_hash(
#                 token, method='sha256'))
#             db.session.add(new_annotator)
#             db.session.commit()
#             login_user(new_annotator, remember=True)
#             flash('Account created!', category='success')
#             return url_for('annotate_data.data',idx=str(0))

#     return render_template("sign_up.html", user=current_user)

@annotator.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return {
        'mesage': 'You have successfully logged out',
        'code': 1,
    }

