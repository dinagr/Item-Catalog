from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Category, Item
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///categorieitems.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

items = session.query(Item).all()
for item in items:
    session.delete(item)
categories = session.query(Category).all()
for category in categories:
    session.delete(category)
session.commit()

category1 = Category(name = "Soccer")
session.add(category1)
session.commit()
item1_1 = Item(category_id = 1, name = "Soccer Socks",
               description = "Soccer socks are extremely "
               "long. They cover shin-guards.")
session.add(item1_1)
session.commit()
item1_2 = Item(category_id = 1, name = "Shin-Guards",
               description = "Shin-guards protect players shins, "
               "a vulnerable part of a players body that often gets kicked.")
session.add(item1_2)
session.commit()
item1_3 = Item(category_id = 1, name = "Soccer Ball",
               description = "Soccer balls allows players to train "
               "and play individually or with friends outside of practice.")
session.add(item1_3)
session.commit()
category2 = Category(name = "Basketball")
session.add(category2)
session.commit()
item2_1 = Item(category_id = 2, name = "Basketball sleeve",
               description = "Made out of nylon and spandex, "
               "it extends from the biceps to the wrist")
session.add(item2_1)
session.commit()
item2_2 = Item(category_id = 2, name = "Basketball uniform",
               description = " Basketball uniforms consist of a jersey "
               "that features the number and last name of the player on "
               "the back, as well as shorts and athletic shoes.")
session.add(item2_2)
session.commit()
item2_3 = Item(category_id = 2, name = "finger sleeve",
               description = "The use of the finger sleeve is authorized"
               "and approved by the NBA (National Basketball Association). "
               "In many cases the finger sleeve is worn for protection instead "
               "of performing some sort of taping job on the digit.")
session.add(item2_3)
session.commit()
item2_4 = Item(category_id = 2, name = "Shot clock",
               description = "It is analogous with the play clock"
               "used in American and Canadian football.")
session.add(item2_4)
session.commit()
category3 = Category(name = "Baseball")
session.add(category3)
category4 = Category(name = "Frisbee")
session.add(category4)
category5 = Category(name = "Snowboarding")
session.add(category5)
category6 = Category(name = "Rock Climbing")
session.add(category6)
category7 = Category(name = "Foosball")
session.add(category7)
category8 = Category(name = "Skating")
session.add(category8)
category9 = Category(name = "Hockey")
session.add(category9)
category10 = Category(name = "Dancing")
session.add(category10)
session.commit()
