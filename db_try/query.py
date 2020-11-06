from sqlalchemy import create_engine, MetaData
from taskrun import users

engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
meta = MetaData()

s = users.select()
conn = engine.connect()
result = conn.execute(s)

"""
SELECT name, email
FROM users
WHERE user.id == taskruns.user_id
AND taskruns.task_type == 'Form'
GROUP BY name
having count(name) > 50
"""
