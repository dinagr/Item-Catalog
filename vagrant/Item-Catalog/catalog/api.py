from catalog import app
from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
import httplib2

# JSON APIs to view Categories and Items Information

# View all categories
@app.route('/categories/JSON')
def categoriesJSON():
    categories = app.db.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

# View all items in a specific category
@app.route('/categories/<string:category_name>/items/JSON')
def categoriesItemsJSON(category_name):
    category = app.db.query(Category).filter(Category.name==category_name).one()
    items = app.db.query(Item).filter(Item.category_id==category.id).all()
    return jsonify(items=[i.serialize for i in items])

# View a specific item
@app.route('/categories/<string:category_name>/items/<string:item_name>/JSON')
def itemJSON(category_name, item_name):
    item = app.db.query(Item).filter(Category.name==category_name,
                                     Item.name==item_name).one()
    return jsonify(item=item.serialize)

