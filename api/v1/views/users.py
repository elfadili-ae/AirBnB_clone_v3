#!/usr/bin/python3
"""
User content view for API.
Create a new view for User objects that
handles all default RESTFul API actions.
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Retrieve all the users"""
    users = storage.all(User)
    if users is None:
        abort(404)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieve a user by user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """Delete a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response("{}", 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """POST a user"""
    res = request.get_json()
    if not res:
        return abort(400, {'message': 'Not a JSON'})
    if 'email' not in res:
        return abort(400, {'message': 'Missing email'})
    if 'password' not in res:
        return abort(400, {'message': 'Missing password'})
    new_user = User(**res)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Update a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    res = request.get_json()
    if res is None:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
