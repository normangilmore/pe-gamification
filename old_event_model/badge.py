from sqlalchemy import Table, Column, Integer, String, MetaData, LargeBinary, ForeignKey
from sqlalchemy import Text, Unicode, UnicodeText, Boolean, Date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from event_model.base import Base

from event_model.utility import make_timestamp


class Badge(Base):
    __tablename__ = "badge"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(length=254), unique=True, nullable=False)

    # Not sure about representing images in SQL Alchemy
    icon = Column(Text, nullable=True)
