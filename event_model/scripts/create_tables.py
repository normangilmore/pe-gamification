from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from event_model.base import Base


# Tables in Gamify Model
from event_model.profile import Profile
from event_model.task_run import TaskRun
from event_model.task import Task
from event_model.project import Project
#from event_model.category import Category
# from event_model.badge import Badge
# from event_model.badge_award import BadgeAward
# from event_model.email_candidate import EmailCandidate
# from event_model.email_purpose import EmailPurpose


def create_gamify_tables(echo=False, returnEngine=False):
    engine = create_engine(
        "postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard",
        echo=echo,
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    print(engine.table_names())
    Base.metadata.drop_all(engine)
    # sql.execute("DROP TABLE IF EXISTS project ", engine)
    Base.metadata.create_all(engine)
    """
    if returnEngine:
        return session, engine
    else:
        return session
    """
    return engine


if __name__ == "__main__":
    engine = create_gamify_tables(False)
    print("finished creating tables")
