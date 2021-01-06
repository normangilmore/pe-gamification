from sqlalchemy import create_engine
from event_model.task_run import TaskRun
from event_model.project import Project
from event_model.user import User
from event_model.task import Task
from event_model.category import Category
from sqlalchemy.orm import sessionmaker
from insert_badges import insert_badges
from query_badge import run_queries
import csv

engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def insert_data(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Run query on user table, if empty, then add new user (result == None)
            in_user = session.query(User).filter(User.id == row['user_id']).first()
            if in_user is None:
                u = User(id=row['user_id'], name=row['name'], email_addr=row['email_addr'])
                session.add(u)
                session.commit()
            # If category not in category table, then add
            in_category = session.query(Category).filter(Category.id == row['category']).first()
            if in_category is None:
                c = Category(id=row['category'], name=row['category_name'])
                session.add(c)
                session.commit()
            # If project not in project table, then add
            in_proj = session.query(Project).filter(Project.id == row['project_id']).first()
            if in_proj is None:
                p = Project(id=row['project_id'],
                            name=row['project_name'],
                            category_id=row['category'])
                session.add(p)
                session.commit()
            # If task not in task table, then add
            in_task = session.query(Task).filter(Task.id == row['task_id']).first()
            if in_task is None:
                t = Task(id=row['task_id'], project_id=row['project_id'])
                session.add(t)
                session.commit()
            # Finally, create taskrun
            tr = TaskRun(created=row['created'], project_id=row['project_id'],
                         task_id=row['task_id'], user_id=row['user_id'],
                         finish_time=row['finish_time'],
                         task_type=row['task_type'])
            session.add(tr)
            session.commit()

if __name__ == "__main__":
    insert_data('taskruns.csv')
    insert_badges('badge_list.csv')
    run_queries()
