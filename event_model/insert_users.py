from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from event_model.base import Base
import pandas as pd


# Tables in Gamify Model
from event_model.task_run import TaskRun
from event_model.task import Task
from event_model.project import Project
from event_model.category import Category
from event_model.user import User
from event_model.badge import Badge
from event_model.badge_award import BadgeAward
from event_model.email_candidate import EmailCandidate
from event_model.email_purpose import EmailPurpose


def create_gamify_tables(echo=False):
    engine = create_engine(
        "postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@"
        "localhost:5432/pe_dashboard",
        echo=echo,
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    return session, engine


if __name__ == "__main__":
    csv_file_path = "/Users/rubywerman/desktop/pe-gamification/"\
                    "ruby-scripts/hi.csv"
    session, engine = create_gamify_tables(False)
    # Read in CSV file
    with open(csv_file_path, 'r') as file:
        data_df = pd.read_csv(file)
    # Go through each row and add to table
    for i in range(len(data_df)):
        try:
            data_df.iloc[i:i+1].to_sql(name="user", index=False,
                                       if_exists='append', con=engine)
        except Exception:
            pass
    result = engine.execute('SELECT * FROM '
                            '"user"')
    for r in result:
        print(r)