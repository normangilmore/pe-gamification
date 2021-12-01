from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from event_model.base import Base
from event_model.helper import dictmaker

# Tables in Gamify Model
from event_model.task_run import TaskRun
from event_model.task import Task
from event_model.project import Project
from event_model.user import User
from event_model.badge import Badge
from event_model.email_candidate import EmailCandidate

import csv

# This code inserts email candidates into the email candidate table
def run_queries():
    engine = create_engine(
        "postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard",
        echo=True,
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    tasks = {"quoted sources" : "a Quoted Sources", "reasoning": "a Reasoning", "probability": "a Probability", "language": "a Language", "form": "a Form", "evidence": "an Evidence", "argument": "an Argument"}
    # Add to email candidate table all users who have done >= 25 tasks per these categories ^^
    metric = 1
    data = []
    for task in tasks:
        query = session.query(User.name, User.email_addr, func.count("*")).join(
            TaskRun).filter(TaskRun.task_type == task).group_by(User.id).having(func.count("*") >= metric).all()
        #print("Query {} results: ".format(task))
        for row in query:
            #in_email = session.query(EmailCandidate).filter(EmailCandidate.to_email_addr == row[1]).filter(EmailCandidate.email_body == "25 " + task).first()
            #print(task, row)
            data.append((row[0], row[1], task, row[2]))

    session.close()
    return data 

if __name__ == "__main__":
    data = run_queries()
    with open("test1.csv", "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(["name", "email", "task", "count"])  # write header
        writer.writerows(data)

