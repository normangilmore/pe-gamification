from sqlalchemy import create_engine, MetaData, select
from taskrun import taskruns, users
import csv

engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
meta = MetaData()
conn = engine.connect()

rows = []
get_user_ids = select([users.c.id])
user_ids = [uid[0] for uid in conn.execute(get_user_ids)]

with open('tr.csv', newline='') as pscfile:
    reader = csv.DictReader(pscfile)
    for row in reader:
        if int(row['user_id']) not in user_ids:
            continue
        r = {'created': row['created'], 'task_id': row['task_id'],
             'user_id': row['user_id'], 'finish_time': row['finish_time'],
             'task_type': row['task_type']}
        rows.append(r)

conn.execute(taskruns.insert(), rows)
