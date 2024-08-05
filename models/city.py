#!/usr/bin/python3
'''
A City module.
'''

from models.base_model import BaseModel, Base
import models
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    '''
    A City class, subclass of BaseModel class with
    public class attributes of type string.
    '''
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        state = relationship('State', back_populates='cities')
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        '''
        Class constructor inherits BaseModel class constructor.
        Initializes instances of a City.
        '''
        super().__init__(*args, **kwargs)
