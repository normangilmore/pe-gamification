from sqlalchemy import create_engine
from event_model.task_run import TaskRun
from event_model.user import User
from event_model.task import Task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, delete
#from create_tables import engine
import csv

engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
Session = sessionmaker(bind = engine)
session = Session()

result = session.execute('SELECT * FROM '
                            '"project"')
for r in result:
    print(r)