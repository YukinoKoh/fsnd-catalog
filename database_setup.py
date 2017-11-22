import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# instance
Base = declarative_base()


# user
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


# mapper
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)


class Option(Base):
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return{
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'cat_id': self.cat_id
        }


class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    option_id = Column(Integer, ForeignKey('options.id'))
    title = Column(String(80), nullable=False)
    url = Column(String(250), nullable=False)


engine = create_engine('sqlite:///researchoption.db')

Base.metadata.create_all(engine) 

