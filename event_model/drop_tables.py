from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from event_model.base import Base

# Tables in Gamify Model
from event_model.task_run import TaskRun
from event_model.task import Task
from event_model.project import Project
from event_model.user import User
from event_model.badge import Badge
from event_model.badge_award import BadgeAward
from event_model.email_candidate import EmailCandidate
from event_model.email_purpose import EmailPurpose
from event_model.category import Category

"""
Use this when debugging and messing with DB strcuture"
"""

def create_gamify_tables(echo=False):
    engine = create_engine(
        "postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard",
        echo=echo,
    )
    print("1")
    Session = sessionmaker(bind=engine)
    print("2")
    session = Session()
    print("3")
    Base.metadata.drop_all(engine)
    print("4")
    session.close()
    return engine


if __name__ == "__main__":
    engine = create_gamify_tables()
