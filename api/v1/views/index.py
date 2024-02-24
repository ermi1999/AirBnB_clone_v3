#!/usr/bin/python3
"""this module implements the views api"""
from api.v1.views import app_views
from flask import jsonify
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from models import storage

@app_views.route('/status')
def status():
    """returns the status of the api"""
    return jsonify({
        "status": "OK"
        })


@app_views.route('/stats')
def stats():
    """returns the the number of each objects."""
    objs = {"amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)}
    return jsonify(objs)
