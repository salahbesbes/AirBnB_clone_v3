#!/usr/bin/python3
""" modules """
from models.state import State
from flask import jsonify, abort, request
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_of_state(state_id):
    """ get all City instance state
    Returns:
        json: list of City instance in the state found
    """
    result = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for obj in state.cities:
        result.append(obj.to_dict())
    return jsonify(result)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """ get city from the database using the storage instance
    Args:
        id (string): id of city instance
    Returns:
        json: in case instance doesn't exist we abord and the
        @app.errorhandler(HTTPException) in app.py file handle it
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return city.to_dict()


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ we delete the instance corresponding on the id sent in the route
    Args:
        id (string): expect to be id of City instance
    Returns:
        json: if case instance doesn't exist we abord and the
        @app.errorhandler(HTTPException) in app.py file handle it
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return {}
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ create new city instance based on the json sent in the request
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

    if storage.get(State, state_id) is None:
        abort(404)

    if req.get('name') is None:
        abort(400, description='Missing name')
    new_city = City(**req, state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ route take as argument the city id, get
        the instance and update it
    Args:
        city_id (string): the city id we want to update
    Returns:
        json: dict of the instance
    """
    try:
        req = request.get_json(force=True)
    except Exception:
        abort(400, description="Not a JSON")
    city_found = storage.get(City, city_id)
    if city_found is None:
        abort(404)
    exclude = ['id', 'created_at', 'updated_at', 'state_id']
    # create a copy of the req without excluded keys
    req = {k: v for k, v in req.items() if k not in exclude}
    for key, val in req.items():
        setattr(city_found, key, val)
    city_found.save()
    storage.save()
    return jsonify(city_found.to_dict()), 200
