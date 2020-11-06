from sqlalchemy import create_engine, MetaData
from taskrun import users
import csv

rows = []
with open('user.csv', newline='') as pscfile:
    # Collect User IDS
    reader = csv.DictReader(pscfile)
    for row in reader:
        r = {'id': row['id'], 'email': row['email'], 'name': row['name']}
        rows.append(r)

engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
meta = MetaData()
conn = engine.connect()
conn.execute(users.insert(), rows)
