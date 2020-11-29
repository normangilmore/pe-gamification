from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Text, Unicode, UnicodeText, Boolean, Date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from event_model.base import Base

from event_model.utility import make_timestamp
from event_model.project import Project
from event_model.task_run import TaskRun


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email_addr = Column(Unicode(length=254), unique=False, nullable=False)
    #: Name of the user (this is used as the nickname).
    name = Column(Unicode(length=254), unique=False, nullable=False)
    # Relationships
    task_runs = relationship(TaskRun, backref="user")
    #projects = relationship(Project, backref="owner")
