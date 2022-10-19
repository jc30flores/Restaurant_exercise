import flask
import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restdb_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurants.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
@app.route("/restaurants")
def restaurants():
    restaurant = session.query(Restaurant).all()
    return render_template('restaurants.html', items=restaurant)

@app.route("/restaurants/new")
def restaurantsNew():
    return "This page is for create a new restaurant"

@app.route("/restaurants/<int:restaurant_id>/edit/")
def restaurantsEdit(restaurant_id):
    return "This page is for edit a restaurant"

@app.route("/restaurants/<int:restaurant_id>/delete/")
def restaurantsDelete(restaurant_id):
    return "This page is for delete a restaurant"


@app.route("/restaurants/<int:restaurant_id>/")
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route("/restaurants/<int:restaurant_id>/new/", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash(f'{newItem.name} Menu Item Created!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit/", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    flash_m = editedItem.name
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name= request.form['name']
        session.add(editedItem)
        session.commit()
        flash(f'{flash_m} Edited to {editedItem.name}!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete/", methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemtodelete = session.query(MenuItem).filter_by(id=menu_id).one()
    flash_m = itemtodelete.name
    if request.method == 'POST':
        session.delete(itemtodelete)
        session.commit()     
        flash(f'{flash_m} Deleted!')   
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=itemtodelete)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenualoneJSON(restaurant_id, menu_id):
    menuitems = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuitems.serialize)



if __name__ == '__main__':
    app.secret_key = "supersecretkey"
    app.debug = True
    app.run(host='0.0.0.0', port=8080)