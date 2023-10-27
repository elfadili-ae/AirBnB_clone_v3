#!/usr/bin/python3
"""
City content view for API.
Create a new view for City objects that
handles all default RESTFul API actions.
"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<path:state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """Get the state's cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<path:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieve a City by city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<path:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """Delete a City by city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response("{}", 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """POST a city by city_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    res = request.get_json()
    if not res:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in res:
        return abort(400, {'message': 'Missing name'})
    res['state_id'] = state_id
    new_city = City(**res)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = request.get_json()
    if res is None:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
