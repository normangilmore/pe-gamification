from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from event_model.base import Base


# Tables in Gamify Model
from event_model.task_run import TaskRun
from event_model.task import Task
from event_model.project import Project
from event_model.profile import Profile


def run_queries():
    engine = create_engine(
        "postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard",
        echo=True,
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    """
    Query 1
    SELECT name, email
    FROM users, taskruns
    WHERE user.id == taskruns.user_id
    AND taskruns.task_type == 'language'
    GROUP BY name
    having count(name) >= 10
    """
    query_1 = session.query(Profile.name, Profile.email_addr, func.count("*")).join(
        TaskRun).filter(TaskRun.task_type == 'language').group_by(Profile.id).having(func.count("*") >= 10).all()
    print("Query 1 results: ")
    for row in query_1:
        print(row)

    """
    Query 2
    SELECT name, email, COUNT(*)
    FROM users
    WHERE user.id == taskruns.user_id
    GROUP BY name
    ORDER BY COUNT(*) DESC
    LIMIT 5
    """

    query_2 = session.query(Profile.name, Profile.email_addr, func.count("*")).join(
        TaskRun).group_by(Profile.id).order_by(func.count("*").desc())[:5]
    print("Query 2 results: ")
    for row in query_2:
        print(row)

    """
    Query 3
    SELECT project_name, COUNT(*)
    FROM taskrun, project
    WHERE project.id == taskruns.project_id
    GROUP BY project.id
    ORDER BY COUNT(*) DESC
    """

    query_3 = session.query(Project.name, func.count("*")).join(
        TaskRun).group_by(Project.id).order_by(func.count("*").desc())
    print("Query 3 results: ")
    for row in query_3:
        print(row)


if __name__ == "__main__":
    run_queries()