from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Text, UnicodeText, Float

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.ext.mutable import MutableDict, MutableList

from event_model.pybossa_model.base import Base

from event_model.utility import make_timestamp
from event_model.pybossa_model.task_run import TaskRun


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

    task_runs = relationship(
        TaskRun, cascade="all, delete, delete-orphan", backref="task"
    )
