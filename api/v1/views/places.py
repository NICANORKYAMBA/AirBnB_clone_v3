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

    all_places = storage.all(Place).values()
    places = (
            [place.to_dict() for place in all_places
                if place.city_id == city_id])
    jsonify(places)


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
    return jsonify({})


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    elif 'user_id' not in data:
        return 'Missing user_id', 400
    elif 'name' not in data:
        return 'Missing name', 400
    user_id = data['user_id']
    user = storage.get('User', user_id)
    if user is None:
        abort(400)

    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
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
    storage.save()
    return jsonify(place.to_dict()), 200
