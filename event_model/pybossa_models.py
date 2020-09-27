from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

Base = declarative_base()

metadata = MetaData()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    #: UTC timestamp of the user when it's created.
    created = Column(Text, default=make_timestamp)
    email_addr = Column(Unicode(length=254), unique=True, nullable=False)
    #: Name of the user (this is used as the nickname).
    name = Column(Unicode(length=254), unique=True, nullable=False)
    #: Fullname of the user.
    fullname = Column(Unicode(length=500), nullable=False)
    #: Language used by the user in the PYBOSSA server.
    locale = Column(Unicode(length=254), default="en", nullable=False)
    admin = Column(Boolean, default=False)
    privacy_mode = Column(Boolean, default=True, nullable=False)
    restrict = Column(Boolean, default=False, nullable=False)
    category = Column(Integer)
    flags = Column(Integer)
    newsletter_prompted = Column(Boolean, default=False)
    valid_email = Column(Boolean, default=False)
    confirmation_email_sent = Column(Boolean, default=False)
    subscribed = Column(Boolean, default=False)
    consent = Column(Boolean, default=False)
    info = Column(MutableDict.as_mutable(JSONB), default=dict())
    user_pref = Column(JSONB)
    notified_at = Column(Date, default=None)

    ## Relationships


#   task_runs = relationship(TaskRun, backref='user')
#   projects = relationship(Project, backref='owner')
#   blogposts = relationship(Blogpost, backref='owner')


class Project(Base):
    __tablename__ = "project"

    #: ID of the project
    id = Column(Integer, primary_key=True)
    #: UTC timestamp when the project is created
    created = Column(Text, default=make_timestamp)
    #: UTC timestamp when the project is updated (or any of its relationships)
    updated = Column(Text, default=make_timestamp, onupdate=make_timestamp)
    #: Project name
    name = Column(Unicode(length=255), unique=True, nullable=False)
    #: Project slug for the URL
    short_name = Column(Unicode(length=255), unique=True, nullable=False)
    #: Project description
    description = Column(Unicode(length=255), nullable=False)
    #: Project long description
    long_description = Column(UnicodeText)
    #: Project webhook
    webhook = Column(Text)
    #: If the project allows anonymous contributions
    allow_anonymous_contributors = Column(Boolean, default=True)
    #: If the project is published
    published = Column(Boolean, nullable=False, default=False)
    # If the project is featured
    featured = Column(Boolean, nullable=False, default=False)
    # If the project owner has been emailed
    contacted = Column(Boolean, nullable=False, default=False)
    #: Project owner_id
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    #: Project Category
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    #: Project info field formatted as JSON
    info = Column(MutableDict.as_mutable(JSONB), default=dict())


#   tasks = relationship(Task, cascade='all, delete, delete-orphan', backref='project')
#   task_runs = relationship(TaskRun, backref='project',
#                            cascade='all, delete-orphan',
#                            order_by='TaskRun.finish_time.desc()')
#   category = relationship(Category)
#   blogposts = relationship(Blogpost, cascade='all, delete-orphan', backref='project')
#   owners_ids = Column(MutableList.as_mutable(ARRAY(Integer)), default=list())


class Task(Base):
    __tablename__ = "task"

    #: Task.ID
    id = Column(Integer, primary_key=True)
    #: UTC timestamp when the task was created.
    created = Column(Text, default=make_timestamp)
    #: Project.ID that this task is associated with.
    project_id = Column(
        Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False
    )
    #: Task.state: ongoing or completed.
    state = Column(UnicodeText, default="ongoing")
    quorum = Column(Integer, default=0)
    #: If the task is a calibration task
    calibration = Column(Integer, default=0)
    #: Priority of the task from 0.0 to 1.0
    priority_0 = Column(Float, default=0)
    #: Task.info field in JSON with the data for the task.
    info = Column(JSONB)
    #: Number of answers to collect for this task.
    n_answers = Column(Integer, default=30)
    #: Array of User IDs that favorited this task
    fav_user_ids = Column(MutableList.as_mutable(ARRAY(Integer)))


#   task_runs = relationship(TaskRun, cascade='all, delete, delete-orphan', backref='task')


class TaskRun(Base):
    __tablename__ = "task_run"

    #: ID of the TaskRun
    id = Column(Integer, primary_key=True)
    #: UTC timestamp for when TaskRun is delivered to user.
    created = Column(Text, default=make_timestamp)
    #: Project.id of the project associated with this TaskRun.
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    #: Task.id of the task associated with this TaskRun.
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"), nullable=False)
    #: User.id of the user contributing the TaskRun (only if authenticated)
    user_id = Column(Integer, ForeignKey("user.id"))
    #: User.ip of the user contributing the TaskRun (only if anonymous)
    user_ip = Column(Text)
    #: UTC timestamp for when TaskRun is saved to DB.
    finish_time = Column(Text, default=make_timestamp)
    timeout = Column(Integer)
    calibration = Column(Integer)
    #: External User ID
    external_uid = Column(Text)
    #: Media URL to an Image, Audio, PDF, or Video
    media_url = Column(Text)
    #: Value of the answer.
    info = Column(JSONB)
