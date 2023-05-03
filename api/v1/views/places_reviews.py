#!/usr/bin/python3
"""Handles all RESTFUL API actions for Review objects"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.review import Review
from flask import abort, jsonify, request


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], stict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    all_reviews = storage.all("Review").values()
    reviews = [
            review.to_dict() for review in reviews
            if review.place_id == place_id]
    return jsonify(reviews)


@app_views.route(
        '/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    new_request = request.get_json
    if new_request is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_request:
        abort(400, 'Missing user_id')
    if 'text' not in new_request:
        abort(400, 'Missing text')
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    new_request['place_id'] = place_id
    new_review = Review(**new_request)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
