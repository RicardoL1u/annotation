from crypt import methods
from flask import Blueprint, render_template, request, flash, jsonify, url_for,redirect
from flask_login import login_required, current_user
# from .models import Note
from . import db
import json
import re
annotate_data = Blueprint('annotate_data', __name__)
dataset = json.load(open('website/company_data.json'))


@annotate_data.route('/pageID=<idx>',methods=['GET','POST'])
@login_required
def data(idx):
    if request.method == 'GET':
        print(f'dump to {idx}')
        idx = int(idx)
        data = dataset[idx]
        ori_topic_entity = re.findall(r'\[.*?\_[0-9]+\]',data['context'])[0]
        return render_template('unit.html',idx=idx, data=data,ori_topic_entity = ori_topic_entity,replace_text = f'<b class="entity", style="color:red">{ori_topic_entity}</b>')
    else:
        print(current_user)
        print(current_user.annotator_name)
        annotated_data = dict(request.form)
        annotated_data['question_text_list'] = json.loads(annotated_data['question_text_list'])
        with open(f"{idx}_{current_user.annotator_name}_{annotated_data['passage_id']}.json",'w') as f:
            json.dump(annotated_data,f,indent=4,ensure_ascii=False)
        return 'hi'


# @annotate_data.route('/submit',methods=['POST'])
# def submit():
#     annotated_data = dict(request.form)
#     annotated_data['question_text_list'] = json.loads(annotated_data['question_text_list'])
#     with open(f"{annotated_data['passage_id']}.json",'w') as f:
#         json.dump(annotated_data,f,indent=4,ensure_ascii=False)
#     return 'hi'




