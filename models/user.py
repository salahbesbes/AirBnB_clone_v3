#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from hashlib import md5
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade='all, delete-orphan')
        reviews = relationship("Review", backref="user",
                               cascade='all, delete-orphan')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        self.password = md5(self.password.encode('utf8')).hexdigest()

    if models.storage_t != 'db':
        @property
        def password(self):
            return self._password

        @password.setter
        def password(self, plain_pass=''):
            self._password = md5(plain_pass.encode('utf8')).hexdigest()
