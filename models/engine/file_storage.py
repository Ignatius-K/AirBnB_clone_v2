#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from re import T


from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    'BaseModel': BaseModel, 'User': User,
    'Place': Place, 'State': State,
    'City': City, 'Amenity': Amenity,
    'Review': Review
}


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if not cls or cls not in classes.values():
            return FileStorage.__objects
        return {
            key: value
            for key, value in FileStorage.__objects.items()
            if type(value) is cls
        }

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """deletes an object from the file"""
        if not obj:
            return
        try:
            obj_type = str(type(obj)).split(".")[-1].split("'")[0]
            del FileStorage.__objects[f'{obj_type}.{obj.id}']
        except Exception:
            pass
        finally:
            self.save()

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def close(self):
        """Close the session"""
        self.reload()
