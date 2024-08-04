#!/usr/bin/python3
"""intitalizes the amenities api."""
from flask import abort, jsonify, request
from models import storage
from models.user import User
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage_t


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities_with_place(place_id):
    """returns all amenities"""
    place = storage.get(Place, place_id)
    if place:
        result = []
        if storage_t == 'db':
            amenities = place.amenities
            for amenity in amenities:
                result.append(amenity.to_dict())
        else:
            for amenity_id in place.amenities:
                result.append(storage.get(Amenity, amenity_id).to_dict())
        return jsonify(result), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_with_place(place_id, amenity_id):
    """deletes a review object"""
    place = storage.get(Place, place_id)
    if place:
        amenity = None
        if storage_t == 'db':
            amenities = place.amenities
            for _obj in amenities:
                if _obj.id == amenity_id:
                    amenity = _obj
        else:
            for _id in place.amenities:
                if _id == amenity_id:
                    amenity = storage.get(Amenity, _id)
        if amenity:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity_with_place_id(place_id, amenity_id):
    """creates a new review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
