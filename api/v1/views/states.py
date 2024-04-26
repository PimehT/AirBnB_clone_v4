#!/usr/bin/python3
""" states module for the API """
from api.v1.views import app_views
from flask import jsonify
from flask import Response
import json
from models import storage
from models.state import State


@app_views.route('/states/', strict_slashes=False, methods=['GET'])
def get_states():
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    response = Response(
        response=json.dumps(states_list, indent=2),
        status=200,
        mimetype='application/json'
    )
    return response


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return json.dumps({"error": "Not found"}, indent=2), 404
    response = Response(
        response=json.dumps(state.to_dict(), indent=2),
        status=200,
        mimetype='application/json'
    )
    return response


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return json.dumps({"error": "Not found"}, indent=2), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', strict_slashes=False, methods=['POST'])
def post_state():
    from flask import request

    data = request.get_json()
    if data is None:
        return json.dumps({"error": "Not a JSON"}, indent=2), 400
    if 'name' not in data:
        return json.dumps({"error": "Missing name"}, indent=2), 400
    state = State(**data)
    state.save()
    response = Response(
        response=json.dumps(state.to_dict(), indent=2),
        status=201,
        mimetype='application/json'
    )
    return response, 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    from flask import request

    state = storage.get(State, state_id)
    if state is None:
        return json.dumps({"error": "Not found"}, indent=2), 404
    data = request.get_json()
    if data is None:
        return json.dumps({"error": "Not a JSON"}, indent=2), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    response = Response(
        response=json.dumps(state.to_dict(), indent=2),
        status=200,
        mimetype='application/json'
    )
    return response, 200
