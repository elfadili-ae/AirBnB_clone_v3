#!/usr/bin/python3
"""
City content view for API.
Create a new view for City objects that
handles all default RESTFul API actions.
"""
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """Get the cities's places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve a place by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """Delete a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response("{}", 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """POST a place in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    res = request.get_json()
    if not res:
        return abort(400, {'message': 'Not a JSON'})
    if 'user_id' not in res:
        return abort(400, {'message': 'Missing user_id'})
    user = storage.get(User, res['user_id'])
    if not user:
        abort(404)
    if 'name' not in res:
        return abort(400, {'message': 'Missing name'})
    res['city_id'] = city_id
    new_place = Place(**res)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = request.get_json()
    if res is None:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
