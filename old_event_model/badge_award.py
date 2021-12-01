from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Text, Unicode, UnicodeText, Boolean, Date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from event_model.base import Base
from event_model.utility import make_timestamp

from event_model.user import User
from event_model.badge import Badge


class BadgeAward(Base):
    __tablename__ = "badge_award"

    # Table to express instance of user and an earned badge
    id = Column(Integer, primary_key=True)

    # Relationships
    user = relationship(User, backref="badge_award")
    badge = relationship(Badge, backref="badge_award")
