#!/usr/bin/python3
""" State Module for HBNB project """
from enum import Enum

from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class StateSchema(Enum):
    """Define State Schema"""
    TABLE_NAME = 'states'
    NAME = 'name'


class State(BaseModel, Base):
    """ State class """

    __tablename__ = StateSchema.TABLE_NAME.value
    name = Column(
        StateSchema.NAME.value, String(128), nullable=False
    )

    # Relationships
    cities = relationship(
        'City', back_populates='state', cascade='all, delete-orphan'
    )
