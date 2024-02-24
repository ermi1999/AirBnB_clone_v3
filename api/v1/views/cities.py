#!/usr/bin/python3
"""intitalizes the cities api."""
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cities_by_state(state_id):
    """returns all cities by state_id"""
    state = storage.get(State, state_id)
    if state:
        cities = state.cities
        result = []
        for city in cities:
            result.append(city.to_dict())
        return jsonify(result), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """gets a city"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """creates a new city"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if state:
        new_city = City(**request.get_json())
        new_city.state_id = state_id
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    else:
        abort(404)

