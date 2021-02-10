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

    tasks = ["quoted sources", "reasoning", "probability", "language", "form", "evidence", "arguments"]
    # Add to email candidate table all users who have done >=10 tasks per these categories ^^
    for task in tasks:
        query = session.query(User.name, User.email_addr, func.count("*")).join(
            TaskRun).filter(TaskRun.task_type == task).group_by(User.id).having(func.count("*") >= 25).all()
        print("Query {} results: ".format(task))
        for row in query:
            in_email = session.query(EmailCandidate).filter(EmailCandidate.to_email_addr == row[1]).filter(EmailCandidate.email_body == "25 " + task).first()
            if in_email is None:
                u = EmailCandidate(to_email_addr=row[1], to_username=row[0], email_body="25 " + task, sendgrid_template_id="d-915ae8191de2421eaa16c43790719632", 
                    sendgrid_info=dictmaker(email=row[1], first_name=row[0], task_name=task, template_id="d-915ae8191de2421eaa16c43790719632"))
                session.add(u)
                session.commit()
    """
    totals = [50, 100]
    # Add total task badges to email candidate table
    for total in totals:
        query = session.query(User.name, User.email_addr, func.count("*")).join(
            TaskRun).group_by(User.id).having(func.count("*") >= total).all()
        print("Query {} tasks results: ".format(total))
        for row in query:
            in_email = session.query(EmailCandidate).filter(EmailCandidate.to_email_addr == row[1]).filter(EmailCandidate.email_body == str(total) + " tasks").first()
            if in_email is None:
                u = EmailCandidate(to_email_addr=row[1], to_username=row[0], email_body=str(total) + " tasks")
                session.add(u)
                session.commit()

    """
if __name__ == "__main__":
    run_queries()
