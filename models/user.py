#!/usr/bin/python3
'''
A User module.
'''

from models.base_model import BaseModel, Base
import models
from os import getenv
from sqlalchemy import Column, String


class User(BaseModel, Base):
    '''
    A User class, subclass of BaseModel class with
    public class attributes of type string.
    '''

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        '''
        Class constructor inherits BaseModel class constructor.
        Initializes instances of a User.
        '''
        super().__init__(*args, **kwargs)
