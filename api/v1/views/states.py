#!/usr/bin/python3
""" modules """
from flask import abort, request
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify


def all_states():
    """ get all State instance from the database
    Returns:
        json: list of State instance
    """
    result = []
    for obj in storage.all(State).values():
        result.append(obj.to_dict())
    return jsonify(result)


def get_state(id):
    """ get state from the database using the storage instance
    Args:
        id (string): id of State instance
    Returns:
        json: if case instance doesn't exist we abord and the
        @app.errorhandler(HTTPException) in app.py file handle it
    """

    for key, obj in storage.all(State).items():
        obj_id = key.split('.')[1]
        if obj_id == id:
            return jsonify(obj.to_dict())
    # if not found raise 404 error
    abort(404, description="Not Found")


def delete_state(id):
    """ we delete the instance corresponding on the id sent in the route
    Args:
        id (string): expect to be id of State instance
    Returns:
        json: if case instance doesn't exist we abord and the
        @app.errorhandler(HTTPException) in app.py file handle it
    """
    key = 'State.' + id
    if key in storage.all(State):
        obj_found = storage.all(State).get(key)
        obj_found.delete()
        storage.save()    # commit all changes
        return {}
    abort(404, description='Not Found')


def create_state():
    """ create new State instance based on the json sent in the request
        if the request doesnt contain a valid json we abord and send a
        description of what happen catched/handled by
        @app.errorhandler(HTTPException) in the app.py file (the root server)
    Returns:
        json: new instance dict created
    """
    try:
        req = request.get_json(force=True)
    except Exception:
        abort(400, description="Not a JSON")
    print(req.get('name'))
    if req.get('name') is None:
        abort(400, description='Missing name')
    new_State = State(**req)
    storage.new(new_State)
    storage.save()
    return jsonify(new_State.to_dict()), 201


def update_state(state_id):
    """ route take as argument the state id, get
        the instance and update it
    Args:
        state_id (string): the state id we want to update
    Returns:
        json: dict of the instance
    """
    try:
        req = request.get_json(force=True)
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")

    obj_found = storage.get(State, state_id)
    if obj_found is None:
        abort(404, description="Not Found")
    req = request.get_json()  # data sent along with the request

    exclude = ['id', 'created_at', 'updated_at']
    # create a copy of the req without excluded keys
    req = {k: v for k, v in req.items() if k not in exclude}
    for key, val in req.items():
        setattr(obj_found, key, val)
    obj_found.save()
    storage.save()
    return jsonify(obj_found.to_dict()), 200


@app_views.route('/states',
                 strict_slashes=False,
                 methods=['GET', 'POST'],
                 defaults={'state_id': None})
@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE', 'PUT', 'GET'])
def handle_State(state_id):
    if state_id:
        if request.method == 'GET':
            return get_state(state_id)
        if request.method == 'PUT':
            return update_state(state_id)
        if request.method == 'DELETE':
            return delete_state(state_id)
    else:
        if request.method == 'GET':
            return all_states()
        if request.method == 'POST':
            return create_state()
