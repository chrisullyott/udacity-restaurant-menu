# Full-Stack-Menu-Project

A simple web app made with Python.

## Dependencies

**Vagrant**
https://www.vagrantup.com/

**SQL Alchemy**
http://www.sqlalchemy.org/

**Flask**
http://flask.pocoo.org/

## Run

Start the vagrant machine:
```$ vagrant up```

Run `finalproject.py`:
```$ python finalproject.py```

The app runs on port `5000`:
```http://localhost:5000/```

## JSON API Endpoints

A JSON API is accessible within the app, available at the following endpoints:

List all restaurants:
```http://localhost:5000/restaurants/json```

List all menu items for a given RESTAURANT_ID:
```http://localhost:5000/restaurants/<RESTAURANT_ID>/menu/json/```

List a single menu item:
```http://localhost:5000/restaurants/<RESTAURANT_ID>/menu/<ITEM_ID>/json/```
