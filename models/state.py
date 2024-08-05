#!/usr/bin/python3
'''
A State module.
'''

from models.base_model import BaseModel, Base
import models
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class State(BaseModel, Base):
    '''
    A State class, subclass of BaseModel class with
    public class attribute of type string.
    '''
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
                'City', back_populates='state',
                )
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        '''
        Class constructor inherits BaseModel class constructor.
        Initializes instances of a State.
        '''
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            '''
            Returns the list of City instances where State.id
            equals to City.state_id
            '''
            city_list = []
            all_cities = models.storage.all(City)
            for value in all_cities.values():
                if self.id == value.state_id:
                    city_list.append(value)
            return city_list
