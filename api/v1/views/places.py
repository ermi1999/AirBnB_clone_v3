#!/usr/bin/python3
"""intitalizes the places api."""
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models import storage_t
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """returns all places"""
    city = storage.get(City, city_id)
    if city:
        result = []
        places = city.places
        for place in places:
            result.append(place.to_dict())
        return jsonify(result), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """gets a place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """deletes a place object"""
    place = storage.get(Place, place_id)
    if place:
        reviews = place.reviews
        for review in reviews:
            storage.delete(review)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """creates a new place object"""
    request_json = request.get_json()
    if not request_json:
        abort(400, "Not a JSON")
    if "user_id" not in request_json:
        abort(400, "Missing user_id")
    if "name" not in request_json:
        abort(400, "Missing name")
    if not storage.get(User, request_json['user_id']):
        abort(404)
    city = storage.get(City, city_id)
    if city:
        new_place = Place(**request.get_json())
        new_place.city_id = city_id
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """updates a place object."""
    if not request.get_json():
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place:
        forbidden_keys = ["id", "user_id",
                          "city_id", "created_at", "updated_at"]
        for key, value in request.get_json().items():
            if key not in forbidden_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """searchs a place objects"""
    request_json = request.get_json()
    if not request_json:
        abort(400, "Not a JSON")
    result = []
    places = storage.all(Place)
    if len(request_json) == 0 or (
            not request_json.get('states') and not request_json.get(
                'cities') and not request_json.get('amenities')):
        for place in places.values():
            result.append(place.to_dict())
        return jsonify(result), 200
    temp = {}
    if 'states' in request_json:
        states = request_json.get('states')
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            temp[place.id] = place

    if 'cities' in request_json:
        cities = request_json.get('cities')
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    temp[place.id] = place

    if 'amenities' in request_json:
        amenity_ids = request_json.get('amenities')
        if request_json.get('cities') or request_json.get('states'):
            for key, value in temp.items():
                for amenity_id in amenity_ids:
                    if storage_t == 'db':
                        ids = []
                        for amenity in value.amenities:
                            ids.append(amenity.id)
                        if amenity_id not in ids:
                            del temp[key]
                    else:
                        if amenity_id not in value.amenities:
                            del temp[key]
        else:
            for value in places.values():
                result.append(value.to_dict())
                for amenity_id in amenity_ids:
                    if storage_t == 'db':
                        ids = []
                        for amenity in value.amenities:
                            ids.append(amenity.id)
                        if amenity_id not in ids:
                            result.pop()
                    else:
                        if amenity_id not in value.amenities:
                            result.pop()
            return jsonify(result)
    for value in temp.values():
        result.append(value.to_dict())
    return jsonify(result), 200
