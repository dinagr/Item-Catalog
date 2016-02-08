import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    @property
    def serialize(self):
        
        return{
            'id': self.id,
            'name' : self.name
            }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String, nullable=False)
    timestmp = Column(DateTime(timezone=True), default=func.now())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        
        return{
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'category_id' : self.category_id,
            'timestmp' : self.timestmp
            }


engine = create_engine('sqlite:///categorieitems.db')


Base.metadata.create_all(engine)
