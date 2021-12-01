from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from event_model.base import Base
from event_model.create_tables import create_gamify_tables
from numpy import genfromtxt


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


def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()


if __name__ == "__main__":
    file_name = "/Users/rubywerman/desktop/pe-gamification/"\
                    "pybossa_api/trainingtasks_taskrun_data.csv"
    session, engine = create_gamify_tables(echo=False, returnEngine=True)
    # Read in taskrun CSV file
    try:
        data = Load_Data(file_name) 
        # Go through each row and add to table
        for i in data:
            record = TaskRun(**{
                'id' : i[0],
                'created' : i[1],
                'project_id' : i[2],
                'task_id' : i[3],
                'user_id' : i[4],                
                'finish_time' : i[5],
                'tasktype': i[6]
            })
            # If user ID isn't in the user table, add info into user data
            # 
            session.add(record) #Add all the records
        session.commit() #Attempt to commit all the records
    #except:
        #print("rollback")
        #session.rollback() #Rollback the changes on error
    finally:
        print("close")
        session.close() #Close the connection

    # How to query for badges:
    # Get all user emails and names that have more than 50 evidence tasks
    # SELECT user, email FROM users WHERE <task> > 50
    result = engine.execute('SELECT * FROM '
                            '"task_run"')
    for r in result:
        print(r)
