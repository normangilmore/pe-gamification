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
from event_model.user import User


class EmailCandidate(Base):
    __tablename__ = "email_candidate"

    # Information for specific email to a user
    id = Column(Integer, primary_key=True)
    to_email_addr = Column(Unicode(length=254), unique=False, nullable=False)
    to_username = Column(Text, nullable=False)
    email_body = Column(Text, nullable=True)

    # Sendgrid specific data
    sendgrid_template_id = Column(Integer)
    sendgrid_info = Column(MutableDict.as_mutable(JSONB), default=dict())
    sent_date = Column(Text, default=make_timestamp)

    # Relationships
    #user = relationship(User, backref="email_candidate")
