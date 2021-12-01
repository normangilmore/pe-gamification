from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Text, UnicodeText, Float

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.ext.mutable import MutableDict, MutableList

from event_model.base import Base

from event_model.utility import make_timestamp
from event_model.task_run import TaskRun


class Task(Base):
    __tablename__ = "task"

    #: Task.ID
    id = Column(Integer, primary_key=True)
    #: Project.ID that this task is associated with.
    project_id = Column(
        Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=True
    )
    #: Task.state: ongoing or completed.
    state = Column(UnicodeText, default="ongoing")
    #: Task.info field in JSON with the data for the task.
    info = Column(JSONB, default="")
    task_runs = relationship(
        TaskRun, cascade="all, delete, delete-orphan", backref="task"
    )
