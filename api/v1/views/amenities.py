#!/usr/bin/python3
"""intitalizes the amenities api."""
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """returns all amenities"""
    amenities = storage.all(Amenity)
    result = []
    for amenity in amenities.values():
        result.append(amenity.to_dict())
    return jsonify(result), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """gets a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def post_amenity():
    """creates a new amenity object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """updates a amenity object."""
    if not request.get_json():
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        forbidden_keys = ["id", "created_at", "updated_at"]
        for key, value in request.get_json().items():
            if key not in forbidden_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
