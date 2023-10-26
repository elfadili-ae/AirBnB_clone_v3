#!/usr/bin/python3
"""API v1"""

from flask import Flask
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

if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    if HBNB_API_HOST == None:
        HBNB_API_HOST = '0.0.0.0'
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_PORT == None:
        HBNB_API_PORT = 5000

    app.run(HBNB_API_HOST, HBNB_API_PORT, threaded=True)
