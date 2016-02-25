# Item Catalog App

## General

This app displays categories and items for every category. </br>
It is possible to add, edit and delete items and categories according to the users authorizations. </br>
If no user is logged into the app, the app will be in a view only state. </br>

### This app was developed using the folowing technologies

1. Python 2.7.6
2. Flask 0.10.1
3. Sqlalchemy 0.8.4
4. OAuth 2.0
5. CSS - bootstrap 3.3.6
6. HTML
7. Vagrant 1.8.1

# Last update date

25/02/2016

### Instructions to activate the app

1. Download the project to your computer
2. Open the command line and go to the 'vagrant' folder
3. Write - 'vagrant up' in the command line
4. Write - 'vagrant ssh' in the command line
5. Write - 'cd /vagrant/Item-Catalog'
6. Now you can activate the app by calling - 'python catalog_app.py'
7. At this Point the app should be available at 'localhost:8000'

### Explenation regarding authorizations in the app

1. When no user is logged into the app is in a view only state.
2. It is possible to log into the app using facbook or google+ acounts
3. Once a user is logged in he can add new categories.
4. Once a user is logged in he can add new items to existing categories (even if these categories were created by other users)
5. A user can edit/delete items only if he created them.
6. A user can edit/delete categories only if he created them.
7. Once a user deletes a category, all the items in this category will be deleted as well (even if they were created by other users)
