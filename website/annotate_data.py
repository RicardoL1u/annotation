from flask import Blueprint, render_template, request, flash, jsonify, url_for,redirect
from flask_login import login_required, current_user
# from .models import Note
from . import db
import json
import re
import os
annotate_data = Blueprint('annotate_data', __name__)
dataset = json.load(open('website/company_data.json'))


@annotate_data.route('/pageID=<idx>',methods=['GET','POST'])
@login_required
def data(idx):
    idx = int(idx)
    data = dataset[idx]
    output_filename = f"{idx}_{current_user.annotator_name}_{data['id']}.json"
    if request.method == 'GET':
        print(f'dump to {idx}')
        
        if os.path.isfile(output_filename):
            filled_values = json.load(open(output_filename))
        else:
            filled_values = {
                "passage_id": data['id'],
                "annoymous_name": "",
                "question_text_list": [
                    {
                        "question_id": q['id'],
                        "question_text": ""
                    } for q in data['questions']
                ]
            }
        ori_topic_entity = re.findall(r'\[.*?\_[0-9]+\]',data['context'])[0]
        return render_template('unit.html',idx=idx,question_num=len(data['questions']), data=data,filled_values=filled_values,ori_topic_entity = ori_topic_entity,replace_text = f'<b class="entity", style="color:red">{ori_topic_entity}</b>')
    else:
        print(current_user)
        print(current_user.annotator_name)
        annotated_data = dict(request.form)
        annotated_data['question_text_list'] = json.loads(annotated_data['question_text_list'])
        with open(output_filename,'w') as f:
            json.dump(annotated_data,f,indent=4,ensure_ascii=False)
        return 'hi'


# @annotate_data.route('/submit',methods=['POST'])
# def submit():
#     annotated_data = dict(request.form)
#     annotated_data['question_text_list'] = json.loads(annotated_data['question_text_list'])
#     with open(f"{annotated_data['passage_id']}.json",'w') as f:
#         json.dump(annotated_data,f,indent=4,ensure_ascii=False)
#     return 'hi'




