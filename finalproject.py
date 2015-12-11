# !flask
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

# !sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

# !database
from restaurants import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# !helpers
from pprint import pprint

# !routing: web app
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
  restaurants = session.query(Restaurant).all()
  return render_template('_page.html', title='Restaurants', view='showRestaurants', restaurants=restaurants)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
  if request.method == 'POST':
    restaurant = Restaurant(name = request.form['name'].strip())
    session.add(restaurant)
    session.commit()
    flash('Restaurant ' + '"' + restaurant.name + '"' + ' created.')
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('_page.html', title='New Restaurant', view='newRestaurant')

@app.route('/restaurants/edit/<int:restaurant_id>/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
  if request.method == 'POST':
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.form['name']:
        restaurant.name = request.form['name'].strip()
    session.add(restaurant)
    session.commit()
    flash('Restaurant ' + '"' + restaurant.name + '"' + ' updated.')
    return redirect(url_for('showRestaurants'))
  else:
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('_page.html', title='Edit Restaurant', view='editRestaurant', restaurant=restaurant)

@app.route('/restaurants/delete/<int:restaurant_id>/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  if request.method == 'POST':
    session.delete(restaurant)
    session.commit()
    flash('Restaurant ' + '"' + restaurant.name + '"' + ' deleted.')
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('_page.html', title='Delete Restaurant', view='deleteRestaurant', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
  return render_template('_page.html', title=restaurant.name, view='showMenu', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  if request.method == 'POST':
    newItem = MenuItem(
      name = request.form['name'].strip(),
      description = request.form['description'].strip(),
      course = request.form['course'].strip(),
      price = request.form['price'].strip(),
      restaurant_id = restaurant.id)
    session.add(newItem)
    session.commit()
    flash('Menu item ' + '"' + newItem.name + '"' + ' created.')
    return redirect(url_for('showMenu', restaurant_id=restaurant_id))
  else:
    return render_template('_page.html', title='New Menu Item', view='newMenuItem', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/edit/<int:menu_item_id>/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_item_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  item = session.query(MenuItem).filter_by(id=menu_item_id).one()
  if request.method == 'POST':
    item.name = request.form['name'].strip()
    item.description = request.form['description'].strip()
    item.course = request.form['course'].strip()
    item.price = request.form['price'].strip()
    session.add(item)
    session.commit()
    flash('Menu item ' + '"' + item.name + '"' + ' updated.')
    return redirect(url_for('showMenu', restaurant_id=restaurant_id))
  else:
    return render_template('_page.html', title='Edit Menu Item', view='editMenuItem', restaurant=restaurant, item=item)

@app.route('/restaurants/<int:restaurant_id>/menu/delete/<int:menu_item_id>/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_item_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  item = session.query(MenuItem).filter_by(id=menu_item_id).one()
  if request.method == 'POST':
    session.delete(item)
    session.commit()
    flash('Menu item ' + '"' + item.name + '"' + ' deleted.')
    return redirect(url_for('showMenu', restaurant_id=restaurant_id))
  else:
    return render_template('_page.html', title='Delete Menu Item', view='deleteMenuItem', restaurant=restaurant, item=item)

# !routing: JSON
@app.route('/restaurants/json/')
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/json/')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/json/')
def restaurantMenuItemJSON(restaurant_id, menu_item_id):
    item = session.query(MenuItem).filter_by(id=menu_item_id).one()
    return jsonify(Item=[item.serialize])

# !run
if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host='0.0.0.0', port=5000)
