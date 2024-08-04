#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import os
from enum import Enum


class STORAGE_TYPE(Enum):
    """Configures the storage"""
    DATABASE = os.getenv('HBNB_TYPE_STORAGE') == 'db'


if STORAGE_TYPE.DATABASE:
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
