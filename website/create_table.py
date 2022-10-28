from enum import unique
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine('sqlite:///database.db', echo = True)
meta = MetaData()

students = Table(
   'annotator', meta, 
   Column('id', Integer, primary_key = True),
   Column('annotator_name', String, unique = True), 
   Column('token', String, unique = True)
#    Column('lastname', String),
)
meta.create_all(engine)