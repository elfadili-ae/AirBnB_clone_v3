#!/usr/bin/python3
"""
index content view for API.
"""

from flask import jsonify
import models
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def view_status():
    """
    status okay for /status
    """
    return jsonify({"status": "OK"})
