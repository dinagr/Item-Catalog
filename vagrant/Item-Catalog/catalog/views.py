from catalog import app
from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
import httplib2
import re

# The main page of the app
# Presents all the categories and the recents added items    
@app.route('/')
@app.route('/main/')
def allCategories():
    categories = app.db.query(Category).all()
    itemsByCategory = app.db.query(Item.name, Category.name).\
                      filter(Item.category_id==Category.id).\
                      order_by(Item.timestmp.desc()).limit(10)
    users = app.db.query(User).all()
    for user in users:
        print(user.name,user.id, user.email, user.picture)
    return render_template('main.html', categories = categories,
                           items = itemsByCategory,
                           login_session = login_session)

# Displays all the items of this category

@app.route('/categories/<string:category_name>/')
def categoryItems(category_name):
    category = app.db.query(Category).filter(Category.name==category_name).one()
    categories = app.db.query(Category).all()
    items = app.db.query(Item.id, Item.name).\
            filter(Item.category_id==category.id).all()
    numOfItems = app.db.query(func.count('*')).\
                 select_from(Item).\
                 filter(Item.category_id==category.id).scalar()
    return render_template('categoryitems.html', 
                           category_user_id = category.user_id,
                           category_name = category.name,
                           items=items, category=category,
                           categories = categories,
                           numOfItems = numOfItems,
                           login_session = login_session)

# Edit category details

@app.route('/categories/<string:category_name>/edit/', methods=['POST','GET'])
def editCategory(category_name):
    category = app.db.query(Category).filter(Category.name==category_name).one()
    if request.method == 'POST':
        category.name=request.form['name']
        app.db.commit()
        flash("The category was edited successfully!")
        return allCategories()
    else:
        return render_template('categoryeditmenu.html',
                               category=category,
                               login_session = login_session)

# Delete a category - this will delete the items in the categoru as well

@app.route('/categories/<string:category_name>/delete/', methods=['POST','GET'])
def deleteCategory(category_name):
    category = app.db.query(Category).filter(Category.name==category_name).one()
    items = app.db.query(Item).filter(Item.category_id==category.id).all()
    if request.method == 'POST':
        for item in items:
            app.db.delete(item)
            app.db.commit()
        app.db.delete(category)
        app.db.commit()
        categories = app.db.query(Category).all()
        flash("The category and the items were deleted successfully!")
        return allCategories()
    else:
        return render_template('categoryideletemenu.html',
                               category = category,
                               login_session = login_session)

# Add a new category to the system

@app.route('/categories/new/', methods=['POST','GET'])
def newCategory():
    if request.method == 'POST':
        inputName = request.form['name'].strip()
        if not inputName:
            flash("Please enter the catgoery name")
            return render_template('newcategoriemenu.html',
                                   login_session = login_session)
        else:
            newCategory = Category(
                name=inputName, user_id = login_session['user_id'])
            app.db.add(newCategory)
            app.db.commit()
            flash("A new category was created successfully!")
            return allCategories()
    else:
        return render_template('newcategoriemenu.html',
                               login_session = login_session)
    
# Display details of a specific item

@app.route('/categories/<string:category_name>/<string:item_name>/',
           methods=['POST','GET'])
def categoryItemDetails(category_name,item_name):
    category = app.db.query(Category).filter(Category.name==category_name).one()
    items = app.db.query(Item).\
            filter(Item.name==item_name, Item.category_id == category.id).one()
    categories = app.db.query(Category).all()
    return render_template('categorieitemmenu.html',
                           categories=categories,
                           items=items,category_name=category.name,
                           login_session = login_session)

# Edit item details

@app.route('/categories/<string:category_name>/<string:item_name>/edit',
           methods=['POST','GET'])
def editCategoryItem(category_name, item_name):
    category = app.db.query(Category).filter(Category.name==category_name).one()
    item = app.db.query(Item).\
           filter(Item.name==item_name, Item.category_id==category.id).one()
    categories = app.db.query(Category).all()
    if request.method == 'POST':
        if(request.form['name']<>''):
            item.name=request.form['name']
        if(request.form['description']<>''):
            item.description=request.form['description']
        if(request.form['picture']<>''):
            item.picture=request.form['picture']
        if(request.form['category']<>''):
            category_name_new=request.form['category']
            categoryNew = app.db.query(Category).\
                          filter(Category.name==category_name_new).one()
            item.category = categoryNew
        app.db.commit()
        items = app.db.query(Item).filter(Item.category_id==category.id).all()
        flash("The item was edited successfully!")
        return render_template('categoryitems.html',
                               category_name=category.name,
                               items=items,
                               categories=categories, category=category
                               ,login_session=login_session)
    else:
        return render_template('editcategorieitemmenu.html',
                               category_name=category_name,
                               item=item, categories=categories,
                               login_session = login_session)

# Delete item

@app.route('/categories/<string:category_name>/<string:item_name>/delete',
           methods=['POST','GET'])
def deleteCategoryItem(category_name, item_name):
    category = app.db.query(Category).filter(Category.name==category_name).one()
    item = app.db.query(Item).\
           filter(Item.name==item_name, Item.category_id==category.id).one()
    categories = app.db.query(Category).all()
    if request.method == 'POST':
        app.db.delete(item)
        app.db.commit()
        items = app.db.query(Item).filter(Item.category_id==category.id).all()
        flash("The item was deleted successfully!")
        return render_template('categoryitems.html',category_name=category.name,
                               items=items, categories=categories,
                               category=category, login_session=login_session)
    else:
        return render_template('deletecategorieitemmenu.html',
                               category_name = category_name,
                               item=item, login_session=login_session)

# Add a new item

@app.route('/categories/<string:category_name>/new/', methods=['POST','GET'])
def newItemInCategory(category_name):
    category = app.db.query(Category).filter(Category.name==category_name).one()
    if request.method == 'POST':
        inputName = request.form['name'].strip()
        inputDescription = request.form['description'].strip()
        inputEmail = request.form['email'].strip()
        if not inputName or not inputDescription:
            flash("Please enter the item name and description")
            return render_template('newitemincategoriemenu.html',
                                   category = category,
                                   login_session=login_session)
        else:
            newItem = Item(
                name=inputName,
                description=inputDescription,
                picture=request.form['picture'],
                category_id=category.id,
                user_id = login_session['user_id'])
            app.db.add(newItem)
            app.db.commit()
            items = app.db.query(Item.id, Item.name).\
                    filter(Item.category_id==category.id).all()
            categories = app.db.query(Category).all()
            flash("The items was created successfully!")
            return render_template('categoryitems.html',
                                   items=items, category_name=category_name,
                                   categories = categories,
                                   login_session=login_session)
    else:
        return render_template('newitemincategoriemenu.html',
                               category = category,
                               login_session=login_session)
