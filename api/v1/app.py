#!/usr/bin/python3
"""API v1"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__, template_folder=app_views)
app.register_blueprint(app_views)
host = getenv('HBNB_API_HOST', '0.0.0.0')
cors = CORS(app, resources={r"/api/v1/*": {"origins": host}})


@app.teardown_appcontext
def teardown(self):
    """Teardown the storage."""
    storage.close()


@app.errorhandler(404)
def _handle_api_error(ex):
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    if HBNB_API_HOST is None:
        HBNB_API_HOST = '0.0.0.0'
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_PORT is None:
        HBNB_API_PORT = 5000

    app.run(HBNB_API_HOST, HBNB_API_PORT, threaded=True)
