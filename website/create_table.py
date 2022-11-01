from sqlalchemy import (
   DATETIME, 
   Boolean, 
   ForeignKey, 
   create_engine, 
   MetaData, 
   Table, 
   Column, 
   Integer, 
   String,
   insert,
   values
)
engine = create_engine('sqlite:///database.db', echo = True)
meta = MetaData()

manager = Table(
   'manager', meta,
   Column('id', Integer, primary_key=True, autoincrement=True), 
   Column('phone',String, unique = True),
   Column('name', String, unique=True, nullable=False),
   Column('token', String,nullable=False),
)

annotator = Table(
   'annotator', meta, 
   Column('id', Integer, primary_key=True, autoincrement=True), 
   Column('phone', String,unique=True),
   Column('name', String, nullable=False,unique = True), 
   Column('token', String,nullable=False),
   Column('manager_phone', Integer, ForeignKey('manager.phone')),
)

passage = Table(
   'passage', meta, 
   Column('id', Integer, primary_key = True, autoincrement = True),
   Column('ori_id', String, unique=True, nullable=False),
   Column('done',Boolean, default=False),
)

annotated_data = Table(
   'annotated_data', meta, 
   Column('id', Integer, primary_key=True, autoincrement=True), 
   Column('passage_ori_id', String, ForeignKey('passage.ori_id')),
   Column('create_timestamp', DATETIME, default = "CURRENT_TIMESTAMP"), 
   Column('annotator_phone', String, ForeignKey('annotator.phone')),
   Column('annotated_filename', String, nullable=False,unique=True), 
)

annotator_task = Table(
   'annotator_task', meta,
   Column('id', Integer, primary_key=True, autoincrement=True),
   Column('annotator_phone', String, ForeignKey('annotator.phone')),
   Column('task_done_number', Integer, default=0),
   Column('passage_id', Integer, ForeignKey('passage.id')),
   Column('passage_ori_id', String, ForeignKey('passage.ori_id')),
   Column('reviewed', Integer, default=0),
   Column('annotated_filename', String, ForeignKey('annotated_data.annotated_filename')),
)

meta.create_all(engine)

import json
from werkzeug.security import generate_password_hash
dataset = json.load(open('../data/company_data.json'))
conn = engine.connect()

conn.execute(passage.insert(),[
      {'ori_id':data['id']}
      for data in dataset
   ]
)

conn.execute(manager.insert(),[
   {'name':'liu','phone':'110','token':generate_password_hash('password',method='sha256')}
])

conn.execute(annotator.insert(),[
      {'name':'liu','phone':'156','token':generate_password_hash('password',method='sha256'),'manager_phone':'110'}
   ]
)
