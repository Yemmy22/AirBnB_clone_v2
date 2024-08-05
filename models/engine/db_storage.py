#!/usr/bin/python3

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class DBStorage():
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes instances of DBStorage
        """
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user,
            password,
            host,
            database,
            pool_pre_ping=True
            ))

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
        Returns all object of the class if class is specfied
        or all existing objects of all class if otherwise
        '''
        if not self.__session:
            self.reload()

        if cls:
            obj_list = self.__session.query(cls)
        else:
            classes = [State, City]
            obj_list = []
            for cls in classes:
                obj_list.extend(self.__session.query(cls))

        all_obj = {}
        for obj in obj_list:
            if obj != '_sa_instance_state':
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                all_obj[key] = obj
        return all_obj

    def new(self, obj):
        '''
        Adds the object to the current session
        '''
        self.__session.add(obj)

    def save(self):
        '''
        Saves the object to the database
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
        Deletes an object from the current database
        session
        '''
        if not self.__session:
            self.reload()
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        session = (sessionmaker(bind=self.__engine,
            expire_on_commit=False))
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session)
