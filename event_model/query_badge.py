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

# This code inserts email candidates into the email candidate table
def run_queries():
    engine = create_engine(
        "postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard",
        echo=True,
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    #tasks = ["quoted sources", "reasoning", "probability", "language", "form", "evidence", "argument"]
    tasks_a = ["quoted sources", "reasoning", "probability", "language", "form"] #seperate vowel and consenant tasks for grammar in the email template
    tasks_an = ["evidence", "argument"]
    # Add to email candidate table all users who have done >= 25 tasks per these categories ^^
    metric = 25
    for task in tasks_a:
        query = session.query(User.name, User.email_addr, func.count("*")).join(
            TaskRun).filter(TaskRun.task_type == task).group_by(User.id).having(func.count("*") >= metric).all()
        print("Query {} results: ".format(task))
        for row in query:
            in_email = session.query(EmailCandidate).filter(EmailCandidate.to_email_addr == row[1]).filter(EmailCandidate.email_body == "25 " + task).first()
            if in_email is None:
                # This is redundant but I'm testing different ways to trigger the emails
                u = EmailCandidate(to_email_addr=row[1], to_username=row[0], email_body="25 " + task, sendgrid_template_id="d-915ae8191de2421eaa16c43790719632", 
                                   sendgrid_info=dictmaker(email=row[1], first_name=row[0], task_name=task, template_id="d-915ae8191de2421eaa16c43790719632"))
                session.add(u)
                session.commit()
    for task in tasks_an:
        query = session.query(User.name, User.email_addr, func.count("*")).join(
            TaskRun).filter(TaskRun.task_type == task).group_by(User.id).having(func.count("*") >= metric).all()
        print("Query {} results: ".format(task))
        for row in query:
            in_email = session.query(EmailCandidate).filter(EmailCandidate.to_email_addr == row[1]).filter(EmailCandidate.email_body == "25 " + task).first()
            if in_email is None:
                # This is redundant but I'm testing different ways to trigger the emails
                u = EmailCandidate(to_email_addr=row[1], to_username=row[0], email_body="25 " + task, sendgrid_template_id="d-64d3613c1a034b6496738f3e688067a8", 
                                   sendgrid_info=dictmaker(email=row[1], first_name=row[0], task_name=task, template_id="d-64d3613c1a034b6496738f3e688067a8"))
                session.add(u)
                session.commit()

    totals = [50] #can add 100, 250, ... later
    # Add total task badges to email candidate table
    for total in totals:
        query = session.query(User.name, User.email_addr, func.count("*")).join(
            TaskRun).group_by(User.id).having(func.count("*") >= total).all()
        print("Query {} tasks results: ".format(total))
        for row in query:
            in_email = session.query(EmailCandidate).filter(EmailCandidate.to_email_addr == row[1]).filter(EmailCandidate.email_body == str(total) + " tasks").first()
            if in_email is None:
                u = EmailCandidate(to_email_addr=row[1], to_username=row[0], email_body=str(total) + " tasks", sendgrid_template_id="d-3097cd29dad94ca3a87ea4469fe4e709", 
                                   sendgrid_info=dictmaker(email=row[1], first_name=row[0], task_name="", template_id="d-3097cd29dad94ca3a87ea4469fe4e709"))
                session.add(u)
                session.commit()

    session.close()           
if __name__ == "__main__":
    run_queries()
