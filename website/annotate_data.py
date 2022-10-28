from flask import Blueprint, render_template, request, flash, jsonify, url_for,redirect
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import re
annotate_data = Blueprint('annotate_data', __name__)
dataset = json.load(open('website/company_data.json'))


@annotate_data.route('/pageID=<idx>')
def data(idx):
    print(f'dump to {idx}')
    idx = int(idx)
    data = dataset[idx]
    ori_topic_entity = re.findall(r'\[.*?\_[0-9]+\]',data['context'])[0]
    return render_template('unit.html',idx=idx, data=data,ori_topic_entity = ori_topic_entity,replace_text = f'<b class="entity", style="color:red">{ori_topic_entity}</b>')



@annotate_data.route('/submit',methods=['POST'])
def submit():
    annotated_data = dict(request.form)
    annotated_data['question_text_list'] = json.loads(annotated_data['question_text_list'])
    with open(f"{annotated_data['passage_id']}.json",'w') as f:
        json.dump(annotated_data,f,indent=4,ensure_ascii=False)
    return 'hi'




