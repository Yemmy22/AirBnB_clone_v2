#!/usr/bin/python3
'''
A BaseModel Module.
'''

from datetime import datetime
import uuid
import models
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel():
    '''
    A BaseModel class. This will be the base class for all
    child classes.
    '''
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(
                DateTime, default=datetime.utcnow(),
                nullable=False
                )
        updated_at = Column(
                DateTime, default=datetime.utcnow(),
                nullable=False
                )

    def __init__(self, *args, **kwargs):
        '''
        Class constructor. Initializes instances of BaseModel
        class and assigns public attributes.
        '''
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        if kwargs:
            for att in kwargs.keys():
                if att == "created_at" or att == "updated_at":
                    setattr(self, att, datetime.fromisoformat(kwargs[att]))
                if att != "__class__":
                    setattr(self, att, kwargs[att])

    def __str__(self):
        '''
        Modifies and return the string representation of the
        BaseModel object.
        '''
        return "[{}] ({}) {}".\
            format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        '''
        Updates the update_at attribute of the object
        and saves the object to a file.
        '''
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        '''
        Appends the object class name to the object dict
        and returns the updated dict object.
        '''
        obj_dict = self.__dict__.copy()
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict["__class__"] = self.__class__.__name__
        if '_sa_instance_state' in obj_dict:
            del obj_dict["_sa_instance_state"]
        return obj_dict

    def delete(self):
        '''
        Deletes the instance from Filestorage
        '''
        model.storage.delete(self)
