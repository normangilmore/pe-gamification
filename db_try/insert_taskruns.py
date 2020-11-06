from sqlalchemy import create_engine, MetaData
from taskrun import taskruns
import csv

rows = []
with open('tr.csv', newline='') as pscfile:
    reader = csv.DictReader(pscfile)
    for row in reader:
        r = {'created': row['created'], 'task_id': row['task_id'],
             'user_id': row['user_id'], 'finish_time': row['finish_time'],
             'task_type': row['task_type']}
        rows.append(r)

engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
meta = MetaData()
conn = engine.connect()
conn.execute(taskruns.insert(), rows)
