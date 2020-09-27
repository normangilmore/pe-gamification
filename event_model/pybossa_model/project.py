from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Text, Unicode, UnicodeText, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.ext.mutable import MutableDict, MutableList

from event_model.pybossa_model.base import Base

from event_model.utility import make_timestamp
from event_model.pybossa_model.task import Task
from event_model.pybossa_model.task_run import TaskRun
from event_model.pybossa_model.category import Category


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

    tasks = relationship(Task, cascade="all, delete, delete-orphan", backref="project")
    task_runs = relationship(
        TaskRun,
        backref="project",
        cascade="all, delete-orphan",
        order_by="TaskRun.finish_time.desc()",
    )
    category = relationship(Category)
    #   blogposts = relationship(Blogpost, cascade='all, delete-orphan', backref='project')
    owners_ids = Column(MutableList.as_mutable(ARRAY(Integer)), default=list())
