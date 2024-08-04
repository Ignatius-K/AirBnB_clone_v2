#!/usr/bin/python3
""" City Module for HBNB project """
from enum import Enum

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class CitySchema(Enum):
    TB_NAME = 'cities'
    NAME = 'name'
    STATE_ID = 'state_id'


class City(BaseModel, Base):
    """ The city class, contains state ID and name """

    __tablename__ = CitySchema.TB_NAME.value
    name = Column(
        CitySchema.NAME.value, String(128), nullable=False
    )
    state_id = Column(
        CitySchema.STATE_ID.value, String(60),
        ForeignKey('states.id'), nullable=False
    )

    # Relationships
    state = relationship('State', back_populates='cities')
