#!/usr/bin/python3
"""Handles all RESTFUL API actions for Place objects"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import abort, jsonify, request


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in places
                   if place['city_id'] == city_id])


@app_views.route(
        '/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    if storage.get(City, city_id) is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore = ['id', 'city_id', 'user_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
