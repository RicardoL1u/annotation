from nturl2path import url2pathname
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# from .models import Annotator
db:SQLAlchemy = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    # from .views import views
    # from .auth import auth
    from .annotate_data import annotate_data
    from .annotator import annotator
    from .manager import manager

    app.register_blueprint(annotate_data, url_prefix='/')
    app.register_blueprint(annotator,url_prefix='/annotator/')
    app.register_blueprint(manager,url_prefix='/manager/')

    # app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')

    from .models import Annotator, Manager

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'annotator.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(phone):
        # Annotator.get()
        # print('user')
        # print(Annotator.query.get(int(id)))
        user = Manager.query.get(phone)
        print('manager')
        print( Manager.query.get(phone))
        print(user.phone)
        if user:
            return user
        else:
            return Annotator.query.get(phone)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
