from sqlalchemy import BOOLEAN, DATETIME, DefaultClause, ForeignKey, create_engine, MetaData, Table, Column, Integer, String
engine = create_engine('sqlite:///database.db', echo = True)
meta = MetaData()

manager = Table(
   'manager', meta,
   Column('phone',String, primary_key = True),
   Column('name', String, unique=True, nullable=False),
)

annotator = Table(
   'annotator', meta, 
   Column('phone', String,primary_key=True),
   Column('name', String, nullable=False,unique = True), 
   Column('token', String,nullable=False, unique = True),
   Column('manager_phone', Integer, ForeignKey('manager.phone')),
   # Column('id', Integer, primary_key = True, autoincrement = True),
)

passage = Table(
   'passage', meta, 
   Column('id', Integer, primary_key = True, autoincrement = True),
   Column('passage_id', String),
   Column('done',BOOLEAN, DefaultClause(False))
)

annotated_data = Table(
   'annotated_data', meta, 
   Column('id', Integer, primary_key=True, autoincrement=True), 
   Column('passage_id', String, ForeignKey('passage.passage_id')),
   Column('create_timestamp', DATETIME, DefaultClause("CURRENT_TIMESTAMP")), 
   Column('annotator_phone', String, ForeignKey('annotator.phone')),
   Column('annotated_filename', String, nullable=False), 
)

annotator_task = Table(
   'annotator_task', meta,
   Column('id', Integer, primary_key=True, autoincrement=True),
   Column('annotator_phone', String, ForeignKey('annotator.phone')),
   Column('task_done_number', Integer, DefaultClause("0")),
   Column('passage_id', String, ForeignKey('passage.passage_id')),
   Column('score', Integer, DefaultClause("0"))
)

meta.create_all(engine)

# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# from models import Annotator, Manager, Annotated_Data
# from werkzeug.security import generate_password_hash, check_password_hash


# db = SQLAlchemy()
# DB_NAME = "database.db"

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
# db.init_app(app)


# new_manager = Manager(manager_name = "test", phone = "123")
# db.session.add(new_manager)
# new_annotator = Annotator(
#    annotator_name = "test_anno", 
#    token = generate_password_hash('123',method='sha256'), 
#    phone = "123",
#    manager_id = 0
# )
# db.session.add(new_annotator)
# db.session.commit()