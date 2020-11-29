from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Text

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from event_model.base import Base

from event_model.utility import make_timestamp


class TaskRun(Base):
    __tablename__ = "taskrun"
    #: ID of the TaskRun
    id = Column(Integer, primary_key=True)
    #: UTC timestamp for when TaskRun is delivered to user.
    created = Column(Text, default=make_timestamp)
    #: Project.id of the project associated with this TaskRun.
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    #: Task.id of the task associated with this TaskRun.
    task_id = Column(Integer, ForeignKey(
        "task.id", ondelete="CASCADE"), nullable=True)
    #: User.id of the user contributing the TaskRun (only if authenticated)
    user_id = Column(Integer, ForeignKey("user.id"))
    #: UTC timestamp for when TaskRun is saved to DB.
    finish_time = Column(Text, default=make_timestamp)
    task_type = Column(JSONB)
