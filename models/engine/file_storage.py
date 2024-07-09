#!/usr/bin/python3
'''
A FileStorage Module.
'''

import json
import os


class FileStorage():
    '''
    A FileStorage class with class attributes to persist all
    objects of the BaseModel class
    '''
    __file_path = "file.json"
    __objects = {}

    def delete(self, obj=None):
        '''
        Deletes input object from file storage
        '''
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def all(self, cls=None):
        '''
        Returns all or all that matches a class of deserialized
        objects in a dict.
        '''
        if cls is not None:
            filtered_obj = {}
            for key, value in self.__objects.items():
                cls_name, i_d = key.split('.')
                if cls_name == cls:
                    filtered_obj[key] = value
                    return filtered_obj
        return self.__objects

    def new(self, obj):
        '''
        Sets in __objects, an initialized object as the value
        of its class name and id - as key - in in the dictionary.
        '''
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        '''
        Replace objects in __objects with the return value of
        to_dict method and serializes __objects in a file.
        '''
        serialized_objects = {}
        for key, value in self.__objects.items():
            serialized_objects[key] = value.to_dict()

        with open(self.__file_path, 'w', encoding="utf-8") as f:
            json.dump(serialized_objects, f)

    def reload(self):
        '''
        Performs a file check and` reloads the into __objects
        deserialzed objects of the BaseModel class, if the
        exists.
        '''

        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding="utf-8") as f:
                try:
                    saved_dict = json.load(f)
                    for name, obj_dict in saved_dict.items():
                        class_name, i_d = name.split('.')
                        from models.base_model import BaseModel
                        from models.user import User
                        from models.state import State
                        from models.city import City
                        from models.place import Place
                        from models.amenity import Amenity
                        from models.review import Review
                        self.__objects[name] = eval(class_name)(**obj_dict)
                except Exception:
                    pass
