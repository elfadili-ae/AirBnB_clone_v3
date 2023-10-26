#!/usr/bin/python3
"""
define blueprint for API.
"""

from flask import blueprints
from api.v1.views.index import *

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')
