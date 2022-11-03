from flask import Blueprint, render_template, request, flash, jsonify, url_for,redirect
from flask_login import login_required, current_user
# from .models import Note
from . import db
import json
from datetime import datetime
from .models import Passage, Annotator, AnnotatorTask, AnnotatedData
annotate_data = Blueprint('annotate_data', __name__)
dataset = json.load(open('data/company_data.json'))


@annotate_data.route('/pageID=<idx>',methods=['GET','POST'])
@login_required
def data(idx):
    if current_user.role != 'annotator':
        return {
            'message': "Only annotators can access this page.",
            'code': 0
        }
    idx = int(idx)
    # if idx not in [unit.passage_id for unit in AnnotatorTask.query.filter_by(annotator_id = current_user.id).all()]:
    task = AnnotatorTask.query.filter_by(annotator_id = current_user.id,passage_id=idx).first()
    if not task:
        return {
            'message': "This annotation task is not available for you",
            'code': 0
        }
    if request.method=='GET':
        data = dataset[idx]
        return {
            'message': "data",
            'data':data,
            'code': 1
        }
    elif request.method=='POST':
        annotated_filename = f'{idx}_{current_user.id}_{task.passage_ori_id}_{task.task_done_number}.json'
        with open('data/'+annotated_filename, 'w') as f:
            json.dump(request.json.get('data'),f,indent=4,ensure_ascii=False)
        task.task_done_number += 1
        task.last_done_timestamp = datetime.now()
        task.task_status = 1
        new_annotated_data = AnnotatedData(
            passage_id=task.passage_id,
            annotator_id=current_user.id,
            annotated_filename=annotated_filename,
        )
        db.session.add(new_annotated_data)
        db.session.add(task)
        db.session.commit()
        return {
            'message': "Annotation Task Done!",
            'code': 1
        }



# @annotate_data.route('/submit',methods=['POST'])
# @login_required
# def submit():
#     annotated_data = dict(request.form)
#     annotated_data['question_text_list'] = json.loads(annotated_data['question_text_list'])
#     with open(f"{annotated_data['passage_id']}.json",'w') as f:
#         json.dump(annotated_data,f,indent=4,ensure_ascii=False)
#     return {
#         'message': "Successful submission",
#         'code': 1
#     }




