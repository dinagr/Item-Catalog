# -*- coding: cp1255 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from math import ceil
import data
app = Flask(__name__)
PER_PAGE = 10

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


engine = create_engine('sqlite:///categorieitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add pagintation

class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
                
# Finish pagintation

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    categories = session.query(Category.name, Category.id).all()
    itemsByCategory = session.query(Item.name, Category.name).filter(Item.category_id==Category.id).order_by(Item.timestmp.desc()).limit(9)
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', categories = categories, items = itemsByCategory, STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        print('get inside the if')
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    print('in the begining')
    if request.args.get('state') != login_session['state']:
        print('inside the condition')
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        print('inside the try')
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        print('inside the except')
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    print(url)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Clean DB before entering data


@app.route('/')
@app.route('/main/')
def allCategories():
    categories = session.query(Category).all()
    itemsByCategory = session.query(Item.name, Category.name).filter(Item.category_id==Category.id).order_by(Item.timestmp.desc()).limit(9)
    return render_template('main.html', categories = categories, items = itemsByCategory)


@app.route('/categories/<int:category_id>/')
def categoryItems(category_id):
    categories = session.query(Category).all()
    items = session.query(Item.id, Item.name).filter(Item.category_id==category_id).all()
    category = session.query(Category.name).filter(Category.id==category_id).one()
    numOfItems = session.query(func.count('*')).select_from(Item).filter(Item.category_id==category_id).scalar()
    return render_template('categoryitems.html', category_id=category_id, items=items, category=category, categories = categories, numOfItems = numOfItems)

@app.route('/categories/<int:category_id>/edit/', methods=['POST','GET'])
def editCategory(category_id):
    category = session.query(Category).filter(Category.id==category_id).one()
    if request.method == 'POST':
        category.name=request.form['name']
        session.commit()
        flash("The category was edited successfully!")
        return allCategories()
    else:
        return render_template('categoryeditmenu.html', category=category) 

@app.route('/categories/<int:category_id>/delete/', methods=['POST','GET'])
def deleteCategory(category_id):
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
        return render_template('categoryideletemenu.html', category = category)


@app.route('/categories/new/', methods=['POST','GET'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'])
        session.add(newCategory)
        session.commit()
        flash("A new category was created successfully!")
        return allCategories()
    else:
        return render_template('newcategoriemenu.html') 

@app.route('/categories/<int:category_id><int:item_id>/', methods=['POST','GET'])
def categoryItemDetails(category_id,item_id):
    items = session.query(Item).filter(Item.id==item_id).one()
    categories = session.query(Category).all()
    return render_template('categorieitemmenu.html',categories=categories, items=items,category_id=category_id)

@app.route('/categories/<int:category_id>/<int:item_id>/edit', methods=['POST','GET'])
def editCategoryItem(category_id, item_id):
    category = session.query(Category.name).filter(Category.id==category_id).one()
    item = session.query(Item).filter(Item.id==item_id).one()
    categories = session.query(Category).all()
    if request.method == 'POST':
        if(request.form['name']<>''):
            item.name=request.form['name']
        if(request.form['description']<>''):
            item.description=request.form['description']
        if(request.form['category']<>''):
            category_name=request.form['category']
            categoryNew = session.query(Category).filter(Category.name==category_name).one()
            item.category = categoryNew
        session.commit()
        items = session.query(Item).filter(Item.category_id==category_id).all()
        flash("The item was edited successfully!")
        return render_template('categoryitems.html',category_id=category_id, items=items, categories=categories, category=category)
    else:
        return render_template('editcategorieitemmenu.html', category_id=category_id, item=item, categories=categories, category=category) 

@app.route('/categories/<int:category_id>/<int:item_id>/delete', methods=['POST','GET'])
def deleteCategoryItem(category_id, item_id):
    category = session.query(Category.name).filter_by(id=category_id).one()
    item = session.query(Item).filter(Item.id==item_id).one()
    categories = session.query(Category).all()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        items = session.query(Item).filter(Item.category_id==category_id).all()
        flash("The item was deleted successfully!")
        return render_template('categoryitems.html',category_id=category_id, items=items, categories=categories, category=category)
    else:
        return render_template('deletecategorieitemmenu.html', category_id = category_id, item=item)

@app.route('/categories/<int:category_id>/new/', methods=['POST','GET'])
def newItemInCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category.id)
        session.add(newItem)
        session.commit()
        items = session.query(Item.id, Item.name).filter(Item.category_id==category_id).all()
        categories = session.query(Category).all()
        flash("The items was created successfully!")
        return render_template('categoryitems.html', category_id=category_id, items=items, category_name =category.name, categories = categories)
    else:
        return render_template('newitemincategoriemenu.html', category = category)

if __name__ == '__main__':
    app.secret_key = 'super_scret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
