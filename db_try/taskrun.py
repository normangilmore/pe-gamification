from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, ForeignKey

engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
meta = MetaData()

users = Table(
   'users', meta,
   Column('id', Integer, primary_key=True),
   Column('email', String),
   Column('name', String),
)

taskruns = Table(
   'taskruns', meta,
   Column('id', Integer, primary_key=True),
   Column('created', Text),
   Column('task_id', Integer),
   Column('user_id', Integer, ForeignKey('users.id')),
   Column('finish_time', Text),
   Column('task_type', String),
)

meta.create_all(engine)
