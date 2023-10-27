#!/usr/bin/python3
"""
Review content view for API.
Create a new view for Review objects that
handles all default RESTFul API actions.
"""
from models import storage
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """Retrieve all the reviews for a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve a review by review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """Delete a review by review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response("{}", 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """POST a review for a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    res = request.get_json()
    if not res:
        return abort(400, {'message': 'Not a JSON'})
    if 'user_id' not in res:
        return abort(400, {'message': 'Missing user_id'})
    user = res['user_id']
    if not user:
        abort(404)
    if 'text' not in res:
        return abort(400, {'message': 'Missing text'})

    res['place_id'] = place_id
    new_review = Review(**res)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    res = request.get_json()
    if res is None:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
