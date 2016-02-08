from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy, Adopter, puppy_adopters
app = Flask(__name__)


engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/main/')
def puppiesMenu():
    puppies = session.query(Puppy).all()
    return render_template('puppiesmenu.html', puppies=puppies)

@app.route('/puppies/<int:puppy_id>/')
def profileMenuPuppy(puppy_id):
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    return render_template('profilepuppymenu.html', puppy=puppy)

# Task 1: Create route for newMenuItem function here

@app.route('/puppies/new/', methods=['POST','GET'])
def newMenuPuppy():
    if request.method == 'POST':
        newPuppy = Puppy(
            name=request.form['name'],
            gender=request.form['gender'],
            dateOfBirth=request.form['dateOfBirth'],
            weight=request.form['weight'],
            picture=request.form['picture'])
        session.add(newPuppy)
        session.commit()
        flash("new puppy was created!")
        return redirect(url_for('puppiesMenu'))
    else:
        return render_template('newpuppymenu.html')
"""
# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem=session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        #item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id)
        editedItem.name=request.form['name']
        session.commit()
        flash("the menu item was edited!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id = menu_id, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here 

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem=session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("the menu item was deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id = menu_id, item=deletedItem)"""

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
