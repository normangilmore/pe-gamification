from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Text

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict, MutableList

from event_model.base import Base

from event_model.utility import make_timestamp

"""
class Category(Base):
    __tablename__ = "category"

    #: Category ID
    id = Column(Integer, primary_key=True)
    #: Name of the Category
    name = Column(Text, nullable=False, unique=True)
    #: Slug for the Category URL
    short_name = Column(Text, nullable=False, unique=True)
    #: Description of the Category
    description = Column(Text, nullable=False)
    #: UTC timestamp when the Category was created
    created = Column(Text, default=make_timestamp)
    #: Info field formatted as JSON for storing additional data
    info = Column(MutableDict.as_mutable(JSONB), default=dict())
"""