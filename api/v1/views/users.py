#!/usr/bin/python3
"""intitalizes the users api."""
from flask import abort, jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_users():
    """returns all users"""
    users = storage.all(User)
    result = []
    for user in users.values():
        result.append(user.to_dict())
    return jsonify(result), 200


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """gets a user"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def post_user():
    """creates a new user object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    new_user = User(**request.get_json())
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """updates a user object."""
    if not request.get_json():
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if user:
        forbidden_keys = ["id", "email", "created_at", "updated_at"]
        for key, value in request.get_json().items():
            if key not in forbidden_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
