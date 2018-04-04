import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()


class Collection(Base):
    __tablename__ = 'collection'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):

        return {
            'name': self.name,
            'id': self.id,
        }


class MovieItem(Base):
    __tablename__ = 'movie_item'

    collection_id = Column(Integer, ForeignKey('collection.id'))
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    year = Column(String(4))
    img = Column(String(250))
    description = Column(String(350))
    collection = relationship(Collection)

    @property
    def serialize(self):

        return {
            'title': self.title,
            'year': self.year,
            'img': self.img,
            'description': self.description,
            'id': self.id,
            'id': self.id,
        }


engine = create_engine('sqlite:///moviecatalogs.db')


Base.metadata.create_all(engine)
