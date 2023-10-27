#!/usr/bin/python3
"""
define blueprint for API.
"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')
"""
blueprint API for airbnb
"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
<<<<<<< HEAD
from api.v1.views.places_amenities import *
=======
>>>>>>> 914dd6f4504daf97b282d72375c0c5775fed126b
