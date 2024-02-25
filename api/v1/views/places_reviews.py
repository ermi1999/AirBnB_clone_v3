#!/usr/bin/python3
"""intitalizes the reviews api."""
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.user import User
from models.review import Review
from models.place import Place
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """returns all reviews"""
    place = storage.get(Place, place_id)
    if place:
        result = []
        reviews = place.reviews
        for review in reviews:
            result.append(review.to_dict())
        return jsonify(result), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """gets a review"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict()), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """deletes a review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """creates a new review object"""
    request_json = request.get_json()
    if not request_json:
        abort(400, "Not a JSON")
    if "user_id" not in request_json:
        abort(400, "Missing user_id")
    if not storage.get(User, request_json['user_id']):
        abort(404)
    new_review = Review(**request.get_json())
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """updates a review object."""
    if not request.get_json():
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if review:
        forbidden_keys = ["id", "user_id",
                          "place_id", "created_at", "updated_at"]
        for key, value in request.get_json().items():
            if key not in forbidden_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
