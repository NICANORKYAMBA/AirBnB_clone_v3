#!/usr/bin/python3
"""Handles all RESTFUL API actions for Review objects"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from flask import abort, jsonify, request


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_reviews = storage.all("Review").values()
    reviews = [
            review.to_dict() for review in all_reviews
            if review.place_id == place_id]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    new_request = request.get_json()
    if new_request is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_request:
        abort(400, 'Missing user_id')
    if 'text' not in new_request:
        abort(400, 'Missing text')
    user = storage.get(User, new_request['user_id'])
    if user is None:
        abort(404)
    new_request['place_id'] = place_id
    new_review = Review(**new_request)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    update_review_json = request.get_json
    if update_review_json is None:
        return jsonify("Not a JSON"), 400
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    review.save()
    for k, v in update_review_json.items():
        if k not in ignore:
            setattr(review, k, v)
            storage.save()
    return jsonify(review.to_dict())
