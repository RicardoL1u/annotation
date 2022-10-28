from flask import Blueprint, render_template, request, flash, jsonify, url_for,redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import Annotator
annotator = Blueprint('annotator', __name__)
# dataset = json.load(open('website/company_data.json'))


@annotator.route('/annotator', methods=['GET', 'POST'])
def anntator():
    if request.method == 'POST':
        annotator_name = request.form.get('annotator_name')
        token = request.form.get('token')

        annotator = Annotator.query.filter_by(annotator_name=annotator_name).first()
        if annotator:
            if check_password_hash(annotator.token, token):
                flash('Logged in successfully!', category='success')
                login_user(annotator, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect token, try again.', category='error')
        else:
            flash('annotator does not exist.', category='error')

    return render_template("login.html", annotator=current_user)





@annotator.route('/annotator_sign_up', methods=['GET', 'POST'])
def anntator_sign_up():
    if request.method == 'POST':
        annotator_name = request.form.get('annotator_name')
        token = request.form.get('token')

        annotator = Annotator.query.filter_by(annotator_name=annotator_name).first()
        print('what')
        if annotator:
            flash('Annotator already exists.', category='error')
        else:
            new_annotator = Annotator(annotator_name=annotator_name, token=generate_password_hash(
                token, method='sha256'))
            db.session.add(new_annotator)
            db.session.commit()
            login_user(new_annotator, remember=True)
            flash('Account created!', category='success')
            return url_for('annotate_data.data',idx=str(123))

    return render_template("sign.html", user=current_user)

@annotator.route('/annotator_logout')
@login_required
def logout_user():
    logout_user()
    return redirect(url_for('annotator.annotator'))
