#!/usr/bin/python3
"""state view"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def states_view():
    """Retrieve all State objects OR post new State"""
    if request.method == "GET":
        states = storage.all("State")
        return jsonify([state.to_dict() for state in states.values()])
    elif request.method == "POST":
        body = request.get_json()
        if not body:
            abort(400, "Not a JSON")
        if 'name' not in body:
            abort(400, "Missing name")
        state = State(**body)
        storage.new(state)
        storage.save()
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def state_view(state_id):
    """Retrieve or delete a state with state_id"""
    state = storage.get(State, state_id)
    if state:
        if request.method == "GET":
            return jsonify(state.to_dict())
        elif request.method == "DELETE":
            storage.delete(state)
            storage.save()
            return make_response(jsonify({}), 200)
        elif request.method == "PUT":
            state_update = request.get_json()
            if not state_update:
                abort(400, "Not a JSON")
            else:
                for key, value in state_update.items():
                    if key not in ["id", "state_id",
                                   "created_at", "updated_at"]:
                        setattr(state, key, value)
            storage.save()
            return make_response(jsonify(state.to_dict()), 200)
    else:
        abort(404)
