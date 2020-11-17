from sqlalchemy import create_engine, MetaData, func, select
from taskrun import users, taskruns
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
meta = MetaData()
conn = engine.connect()

# u = users.select()
# tr = taskruns.select()
# user_result = conn.execute(u)
# taskruns_result = conn.execute(tr)

"""
SELECT name, email
FROM users
WHERE user.user_id == taskruns.user_id
AND taskruns.task_type == 'Form'
GROUP BY name
having count(name) > 50
"""

# did not use having clause because none of these results seem to have over 50 task runs
join_stmt = users.join(taskruns)
test_query = select([users.c.name, func.count(users.c.name)]).select_from(join_stmt).where(taskruns.c.task_type == "Form").group_by(users.c.id)
result = conn.execute(test_query).fetchall()
for r in result:
    print(r)
    
# test_query = session.query(
#     User).join(
#         Taskrun, Taskrun.c.user_id == User.c.user_id).filter(
#             Taskrun.c.task_type == 'Form').group_by(
#                 User.c.user_id).all()
# s