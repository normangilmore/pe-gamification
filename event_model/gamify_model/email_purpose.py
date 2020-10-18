from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Text, Unicode, UnicodeText, Boolean, Date, TIMESTAMP

# from sqlalchemy.types import Timestamp

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from event_model.gamify_model.base import Base

from event_model.utility import make_timestamp
from event_model.gamify_model.badge_award import BadgeAward
from event_model.gamify_model.email_candidate import EmailCandidate


class EmailPurpose(Base):
    # each entry will tell us: to keep track of candidate email purposes, only used for candidates intended to notify user of new badge being earned
    __tablename__ = "email_purpose"

    id = Column(Integer, primary_key=True)
    date = Column('date', TIMESTAMP(timezone=True))
    # Relationships
    email_candidate = relationship(EmailCandidate, backref="email_candidate")
    badge_award = relationship(BadgeAward, backref="badge_award")
