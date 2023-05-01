#!/usr/bin/python3
"""Handles all default RESTful API actions for User object"""
from models import storage
from models.user import User
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves a list of all user objects"""
    users_list = []
    for user in storage.all(User).values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    data = request.get_json()
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        ignore = ['id', 'email', 'updated_at', 'updated_at']
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict())
