#!/usr/bin/python3
"""
City content view for API.
Create a new view for City objects that
handles all default RESTFul API actions.
"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """Retrieve all the amenities"""
    amenities = storage.all(Amenity)
    if amenities is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve an Amenity by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Delete a amenity by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response("{}", 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """POST an amenity"""
    res = request.get_json()
    if not res:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in res:
        return abort(400, {'message': 'Missing name'})
    new_amenity = Amenity(**res)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Update an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    res = request.get_json()
    if res is None:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
