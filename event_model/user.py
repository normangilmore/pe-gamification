from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Text, Unicode, UnicodeText, Boolean, Date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from event_model.pybossa_model.base import Base

from event_model.utility import make_timestamp
from event_model.pybossa_model.project import Project
from event_model.pybossa_model.task_run import TaskRun


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
    #   notified_at = Column(Date, default=None)

    ## Relationships
    task_runs = relationship(TaskRun, backref="user")
    projects = relationship(Project, backref="owner")
