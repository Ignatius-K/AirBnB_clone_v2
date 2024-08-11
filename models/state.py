#!/usr/bin/python3
""" State Module for HBNB project """
from enum import Enum
from typing import List

import os
import models
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City


class StateSchema(Enum):
    """Define State Schema"""
    TABLE_NAME = 'states'
    NAME = 'name'


class State(BaseModel, Base):
    """ State class """
    is_database = os.getenv('HBNB_TYPE_STORAGE') == 'db'

    if is_database:
        __tablename__ = StateSchema.TABLE_NAME.value
        name = Column(StateSchema.NAME.value, String(128), nullable=False)
        # Relationships
        _cities = relationship(
            'City',
            back_populates='state',
            cascade='all, delete-orphan'
        )
    else:
        name = ""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    @property
    def cities(self) -> List[City]:
        if self.is_database:
            return self._cities
        else:
            return list(
                filter(
                    lambda x: x.state_id == self.id,
                    models.storage.all(City)
                )
            )
