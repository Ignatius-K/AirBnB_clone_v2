#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

from sqlalchemy import create_engine
import os
from enum import Enum

from sqlalchemy.orm import scoped_session, sessionmaker

from models.base_model import Base
from models.state import State
from models.city import City


class ENVIRONMENT(Enum):
    """Define the Environment enum"""
    DEVELOPMENT = 'dev'
    TEST = 'test'
    PRODUCTION = 'production'


class DB_CONFIG(Enum):
    """Define the database config"""
    USER = os.getenv('HBNB_MYSQL_USER')
    USER_PASSWD = os.getenv('HBNB_MYSQL_PWD')
    HOST = os.getenv('HBNB_MYSQL_HOST', 'localhost')
    NAME = os.getenv('HBNB_MYSQL_DB')
    ENVIRONMENT = os.getenv('HBNB_ENV')


classes = {
    'City': City,
    'State': State
}


def get_key_for_class(_class):
    """Get key of class"""
    for key, value in classes.items():
        if value == _class:
            return key
    return None


class DBStorage:
    """This class defines the database storage interface

    Implemented based on SQLAlchemy,
    describes the engine creating the aplication to database session

    Attributes:
        __engine: SQLAlchemy's engine
        __session: SQLAlchemy's Session instance
    """

    __engine = None
    __session = None

    def __init__(self) -> None:
        self.__engine = create_engine(
            f'mysql+pymysql://' +
            f'{DB_CONFIG.USER.value}:{DB_CONFIG.USER_PASSWD.value}@' +
            f'{DB_CONFIG.HOST.value}/{DB_CONFIG.NAME.value}',
            connect_args={'ssl_disabled': True},
            pool_pre_ping=True
        )
        if DB_CONFIG.ENVIRONMENT.value == ENVIRONMENT.TEST.value:
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        items = {}
        if cls:
            if cls in classes.values():
                for item in self.__session.query(cls).all():
                    items[f'{get_key_for_class(cls)}.{item.id}'] = item
            else:
                raise ValueError("Class not recognized")
        else:
            for model_name, model in classes.items():
                for item in self.__session.query(model).all():
                    items[f'{model_name}.{item.id}'] = item
        return items

    def new(self, obj):
        """Adds new object to session"""
        self.__session.add(obj)

    def save(self):
        """Saves storage dictionary to file"""
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def delete(self, obj=None):
        """deletes an object from the file"""
        if not obj:
            return None
        try:
            self.__session.delete(obj)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def reload(self):
        """Loads the db"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory=session_factory)
        self.__session = Session()

    def close(self):
        """Close session"""
        # self.__session.close()
        self.__session.remove()
