from sqlalchemy import create_engine
from event_model.task_run import TaskRun
from event_model.project import Project
from event_model.user import User
from event_model.task import Task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import csv

engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
Session = sessionmaker(bind = engine)
session = Session()

# So i don't go crazy reading the traceback in terminal
for i in range(1000):
    print(" ")

# Select all users and emails with over 5 evidence tasks
#SELECT User.name, User.email_addr FROM user, taskruns 

#print out to see our baby :')
result = engine.execute('SELECT * FROM '
                            '"user"')
for r in result:
    print(r)


"""
code to print out tables
m = MetaData()
m.reflect(engine)
for table in m.tables.values():
    print(table.name)
    #for column in table.c:
      #  print(column.name)
"""

"""
code to print out tables
m = MetaData()
m.reflect(engine)
for table in m.tables.values():
    print(table.name)
    #for column in table.c:
      #  print(column.name)
"""