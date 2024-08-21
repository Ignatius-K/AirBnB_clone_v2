#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os
from enum import Enum


class STORAGE_TYPE(Enum):
    """Configures the storage"""
    DATABASE = 'db'
    FILE = 'fs'


is_database = STORAGE_TYPE.DATABASE == os.getenv('HBNB_TYPE_STORAGE')
if is_database:
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
