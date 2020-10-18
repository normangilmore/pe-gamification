from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Text, Unicode, UnicodeText, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.ext.mutable import MutableDict, MutableList

from event_model.gamify_model.base import Base

from event_model.utility import make_timestamp
from event_model.gamify_model.task import Task
from event_model.gamify_model.task_run import TaskRun
from event_model.gamify_model.category import Category


class Project(Base):
    __tablename__ = "project"

    #: ID of the project
    id = Column(Integer, primary_key=True)
    #: Project name
    name = Column(Unicode(length=255), unique=True, nullable=False)
    #: Project slug for the URL
    short_name = Column(Unicode(length=255), unique=True, nullable=False)
    #: Project Category
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    #: Project info field formatted as JSON
    info = Column(MutableDict.as_mutable(JSONB), default=dict())
    tasks = relationship(
        Task, cascade="all, delete, delete-orphan", backref="project")
    task_runs = relationship(
        TaskRun,
        backref="project",
        cascade="all, delete-orphan",
        order_by="TaskRun.finish_time.desc()",
    )
    category = relationship(Category)
