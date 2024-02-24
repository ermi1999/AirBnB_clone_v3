#!/usr/bin/python3
"""implements all default RESTFul API actions on the states object"""
from flask import abort, jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_get(state_id=None):
    """gets all state objects"""
    _objs = storage.all(State)
    if state_id:
        _id = "State.{}".format(state_id)
        _obj = _objs.get(_id)
        if _obj:

            return jsonify(_obj.to_dict())
        else:
            abort(404)
    _all = []
    for value in _objs.values():
        _all.append(value.to_dict())
    return jsonify(_all)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def states_delete(state_id):
    """deletes the state object that matches the state_id"""
    if state_id:
        _objs = storage.all(State)
        _id = "State.{}".format(state_id)
        _obj = _obj.get(_id)
        if _obj:
            storage.delete(_obj)
            storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """adds a new data to the states object"""
    if not request.get_json():
        abort(400, {"message": "Not a JSON"})
    if 'name' not in request.get_json():
        abort(400, {"message": "Missing name"})
    new_obj = State(**request.get_json())
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def states_put(state_id):
    """updates the state object"""
    if not request.get_json():
        abort(400, "Not a json")
    _id = "State.{}".format(state_id)
    _obj = storage.all().get(_id)
    not_allowed = ["id", "created_at", "updated_at"]
    for key, value in request.get_json().items():
        if key not in not_allowed:
            setattr(_obj, key, value)
    storage.save()
    return jsonify(_obj.to_dict()), 200
