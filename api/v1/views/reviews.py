#!/usr/bin/python3
"""Handles all RESTFUL API actions for Review objects"""
from api.v1.views import app_views
from flask import Blueprint
from models import storage
from models.place import Place
from models.review import Review
from flask import abort, jsonify, request


@app_views.route(
    '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = storage.all(Review).values()
    return jsonify([review.to_dict() for review in reviews
                   if review['place_id'] == place_id])


@app_views.route(
        '/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews(review_id):
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
    if storage.get(Place, place_id) is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore = ['id', 'place_id', 'user_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
