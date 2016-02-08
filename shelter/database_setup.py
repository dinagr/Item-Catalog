import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)


class Puppy(Base):
    __tablename__ = 'puppy'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    picture = Column(String)
#    shelter_id = Column(Integer, ForeignKey('shelter.id'))
#   adopter_id = Column(Integer, ForeignKey('adopter.id'))
#    shelter = relationship("Shelter", back_populates="puppy")
 #   adopter = relationship("Adopter", secondary = association_table, back_populates="adopter")
    weight = Column(Numeric(10))

"""association_table = Table('association', Base.metadata,
    Column('adopter', Integer, ForeignKey('adopter.id')),
    Column('puppy', Integer, ForeignKey('puppy.id'))
)

class Adopter(Base):
    __tablename__ = 'adopter'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship("Puppy", secondary = association_table)"""



engine = create_engine('sqlite:///puppyshelter.db')


Base.metadata.create_all(engine)
