# -*- coding: cp1255 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
app = Flask(__name__)


engine = create_engine('sqlite:///categorieitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Clean DB before entering data

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

@app.route('/')
@app.route('/main/')
def allCategories():
    categories = session.query(Category).all()
    itemsByCategory = session.query(Item.name, Category.name).filter(Item.category_id==Category.id).order_by(Item.timestmp.desc()).limit(9)
    return render_template('main.html', categories = categories, items = itemsByCategory)


@app.route('/categories/<int:category_id>/')
def categoryItems(category_id):
    categories = session.query(Category).all()
    items = session.query(Item.name).filter(Item.category_id==category_id).all()
    category = session.query(Category.name).filter(Category.id==category_id).one()
    return render_template('categoryitems.html', category_id=category_id, items=items, category=category, categories = categories)

@app.route('/categories/<int:category_id>/edit/')
def editCategory(category_id):
    category = session.query(Category).filter(Category.id==category_id).one()
    return render_template('categoryeditmenu.html', category=category)

@app.route('/categories/<int:category_id>/delete/')
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter(Item.category_id==category_id).all()
    if request.method == 'POST':
       # for item in items:
        #    session.delete(item)
         #   session.commit()
        session.delete(category)
        session.commit()
        flash("The category and the items were deleted successfully!")
        return allCategories()
    else:
        return render_template('categoryideletemenu.html', category = category)


@app.route('/categories/new/', methods=['POST','GET'])
def newCategory():
    if request.method == 'POST':
        print(request.form['name'])
        newCategory = Category(
            name=request.form['name'])
        session.add(newCategory)
        session.commit()
        flash("A new category was created successfully!")
        return allCategories()
    else:
        return render_template('newcategoriemenu.html') 

@app.route('/categories/<int:category_id>/<int:item_id>/', methods=['POST','GET'])
def categoryItemDetails(category_id, item_id):
    return render_template('categorieitemmenu.html')

@app.route('/categories/<int:category_id>/<int:item_id>/edit', methods=['POST','GET'])
def editCategoryItem(category_id, item_id):
    return render_template('editcategorieitemmenu.html')

@app.route('/categories/<int:category_id>/<int:item_id>/delete', methods=['POST','GET'])
def deleteCategoryItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter(Item.category_id==category_id).all()
    if request.method == 'POST':
        for item in items:
            session.delete(item)
            session.commit()
        session.delete(category)
        session.commit()
        flash("The category and the items were deleted successfully!")
        return allCategories()
    else:
        return render_template('deletecategorieitemmenu.html', category = category)
    return render_template('deletecategorieitemmenu.html')

@app.route('/categories/<int:category_id>/new/', methods=['POST','GET'])
def newItemInCategory(category_id):
    return render_template('newitemincategoriemenu.html')

if __name__ == '__main__':
    app.secret_key = 'super_scret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
