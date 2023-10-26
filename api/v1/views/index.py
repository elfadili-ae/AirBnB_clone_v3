#!/usr/bin/python3
"""index"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route("/status", strict_slashes=False)
def status():
    return jsonify(status="OK")

@app_views.route("/stats", strict_slashes=False)
def stats():
    amenities = storage.count("Amenity")
    cities = storage.count("City")
    places = storage.count("Place")
    reviews = storage.count("Review")
    states = storage.count("State")
    users = storage.count("User")
    return jsonify(amenities=amenities,
                   cities=cities,
                   places=places,
                   reviews=reviews,
                   states=states,
                   users=users)
