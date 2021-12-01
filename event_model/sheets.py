"""
A Python script that reads the result of a SQL query into a DataFrame
and then pushes those results into a Google Spreadsheet.
"""
import gspread
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc, create_engine
from event_model.task_run import TaskRun
from event_model.task import Task
from event_model.project import Project
from event_model.profile import Profile
from sqlalchemy.sql import func
from event_model.base import Base
from gspread.exceptions import APIError, SpreadsheetNotFound, \
    WorksheetNotFound

# Declaring all variables upfront so you can easily edit and use
drivername = 'postgresql'
user = 'pe_dashboard'
password = 'test-only-yVu8W5azUtZ8RPSWX42o'
host = 'localhost'  # Change this depending on your host. 
port = '5432'  # Change this to reflect your port. 
db_name = 'pe_dashboard'

# Query we want to run. Preferably, only read-only query

    # SELECT name, email, COUNT(*)
    # FROM users
    # WHERE user.id == taskruns.user_id
    # GROUP BY name
    # ORDER BY COUNT(*) DESC
    # LIMIT 5
# Name of Google Sheets file 
google_sheets_file_name = 'Gamification Test'

# Name of the Google Sheet tab we want to write to
google_sheets_tab_name = 'taskrun1'

CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}".format(
    drivername=drivername,
    user=user,
    passwd=password,
    host=host,
    port=port,
    db_name=db_name
)

try:
    engine = create_engine(CONNECTION_STRING)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = "SELECT name, COUNT(*) FROM profile LEFT JOIN taskrun ON profile.id = user_id GROUP BY name ORDER BY COUNT(*) DESC"
    data = pd.read_sql_query(query, engine)
except exc.SQLAlchemyError as e:
    print(e)
    exit("Please check the error above and fix it. Exiting now.")


# A few transformations below as an example.
def date_to_string(date):
    if date is not None:
        if pd.core.dtypes.common.is_datetime_or_timedelta_dtype(date):
            return date.dt.strftime('%y-%m-%d %H:%M:%S')


# Transform timestamp column to string so that we don't get the error below:
# TypeError: Object of type 'Timestamp' is not JSON serializable
if 'created_at' in data:
    data['created_at'] = date_to_string(data['created_at'])
if 'updated_at' in data:
    data['updated_at'] = date_to_string(data['updated_at'])

# Fill up Nan Values with empty string to avoid Invalid JSON payload error.
data.fillna('', inplace=True)

try:
    gs = gspread.oauth()
except FileNotFoundError as e:
    exit("Config files not found. Normally set in ~/.config/gspread directory. Please refer to documentation.")

try:
    sheet = gs.open(google_sheets_file_name)
    ws = sheet.worksheet(google_sheets_tab_name)
    updated = ws.update([data.columns.values.tolist()] + data.values.tolist())
except SpreadsheetNotFound:
    exit("Google Sheet not found. Please make sure you have a Google Sheet named %s" % google_sheets_file_name)
except WorksheetNotFound:
    exit("Worksheet not found. Please make sure you have a worksheet named %s" % google_sheets_tab_name)
except APIError as e:
    exit(e.response.text)
except TypeError as e:
    exit(e)