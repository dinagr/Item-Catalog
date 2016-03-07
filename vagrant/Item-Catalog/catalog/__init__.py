from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

engine = create_engine('postgresql+psycopg2://catalog:catalogLinuxWebServer@localhost/categorieitems')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
import data
app = Flask(__name__)
app.db = session
# Loging in and loging out with google plus anf facebook functionality
import catalog.signin
# The app functionality
import catalog.views
# API
import catalog.api

