from flask import Blueprint, render_template, request, flash, jsonify, url_for,redirect
from flask_login import login_required, current_user
from flask import send_file
from glob import glob
from io import BytesIO
from zipfile import ZipFile
import os
# from .models import Note
from . import db
import json
import pytz
from datetime import datetime
from hashlib import sha256
from .models import Passage, Annotator, AnnotatorTask, AnnotatedData
annotate_data = Blueprint('annotate_data', __name__)
dataset = {v['id']:v for v in json.load(open('resource/company_data_0.8.json'))}


@annotate_data.route('/pageID=<hash_id>',methods=['GET','POST'])
@login_required
def data(hash_id):
    if current_user.role != 'annotator':
        return {
            'message': "Only annotators can access this page.",
            'code': 0
        }
    if hash_id not in dataset.keys():
        return {
            'message': "passage doesn't exist",
            'code': 0
        }
    task = AnnotatorTask.query.filter_by(annotator_id = current_user.id,passage_ori_id=hash_id).first()
    if not task:
        passage = Passage.query.filter_by(ori_id=hash_id).first()
        task = AnnotatorTask(
            annotator_id=current_user.id, 
            passage_id=passage.id,
            passage_ori_id = passage.ori_id
        )
        db.session.add(task)
        db.session.commit()
    if request.method=='GET':
        data = dataset[hash_id] # because the database passage index starts at 1 !!!!!
        if 'altLabel' not in data['topic_entity']['zh'].keys():
            data['topic_entity']['zh']['altLabel'] = []
        return {
            'message': "data",
            'data':data,
            'code': 1
        }
    elif request.method=='POST':
        annotated_filename = f'{task.passage_id}_{current_user.id}_{task.passage_ori_id}_{task.task_done_number}'
        annotated_filename = sha256(annotated_filename.encode()).hexdigest()+'.json'
        with open('data/'+annotated_filename, 'w') as f:
            json.dump(request.json.get('data'),f,indent=4,ensure_ascii=False)
        task.task_done_number += 1
        task.last_done_timestamp = datetime.now(pytz.timezone('Asia/Hong_Kong')
        task.annotated_filename = annotated_filename
        task.task_status = 1
        new_annotated_data = AnnotatedData(
            passage_ori_id=task.passage_ori_id,
            annotator_id=current_user.id,
            annotated_filename=annotated_filename,
        )
        db.session.add(new_annotated_data)
        db.session.add(task)
        db.session.commit()
        return {
            'message': "Annotation Task Done!",
            'annotated_filename': annotated_filename[:-5],
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



@annotate_data.route("/download", methods=["POST"])
@login_required
def download():
    if current_user.role == "annotator":
        data_list = AnnotatedData.query.filter_by(annotator_id=current_user.id).all()
    elif current_user.role == "manager":
        annotators = Annotator.query.filter_by(manager_id=current_user.id).all()
        data_list = []
        for annotator in annotators:
            data_list.extend(AnnotatedData.query.filter_by(annotator_id=annotator.id).all())
    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for file in [data.annotated_filename for data in data_list]:
            zf.write(os.path.join('data',file), os.path.basename(file))
    stream.seek(0)

    return send_file(
        stream,
        as_attachment=True,
        download_name='archive.zip'
    )
