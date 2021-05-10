#!/usr/bin/python3
""" modules """
from api.v1.views.states import all_states
from models.place import Place
from flask import abort, json, request
from models.city import City
from models.user import User
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, redirect, url_for
from api.v1.views.cities import cities_of_state


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def places_of_city(city_id):
    """ get all place instance city
    Returns:
        json: list of place instance in the city found
    """
    result = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for obj in city.places:
        result.append(obj.to_dict())
    return jsonify(result)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """ get place from the database using the storage instance
    Args:
        id (string): id of place instance
    Returns:
        json: in case instance doesn't exist we abord and the
        @app.errorhandler(HTTPException) in app.py file handle it
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ we delete the instance corresponding on the id sent in the route
    Args:
        id (string): expect to be id of place instance
    Returns:
        json: if case instance doesn't exist we abord and the
        @app.errorhandler(HTTPException) in app.py file handle it
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return {}
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ create new place instance based on the json sent in the request
        if the request doesnt contain a valid json we abord and send a
        description of what happen catched/handled by
        @app.errorhandler(HTTPException) in the app.py file (the root server)
    parms:
        (city_id): id if City
    Returns:
        json: new instance dict created
    """

    try:
        req = request.get_json(force=True)
    except Exception:
        abort(400, description="Not a JSON")

    if storage.get(City, city_id) is None:
        abort(404)

    if req.get('name') is None:
        abort(400, description='Missing name')
    user_id = req.get('user_id')
    if user_id is None:
        abort(400, description='Missing user_id')
    current_user = storage.get(User, user_id)
    if current_user is None:
        abort(404)
    new_place = Place(city_id=city_id, **req)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ route take as argument the place id, get
        the instance and update it
    Args:
        place_id (string): the place id we want to update
    Returns:
        json: dict of the instance
    """
    try:
        req = request.get_json(force=True)
    except Exception:
        abort(400, description="Not a JSON")
    place_found = storage.get(Place, place_id)
    if place_found is None:
        abort(404)
    exclude = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']
    # create a copy of the req without excluded keys
    req = {k: v for k, v in req.items() if k not in exclude}
    for key, val in req.items():
        setattr(place_found, key, val)
    place_found.save()
    storage.save()
    return jsonify(place_found.to_dict()), 200


def all_places_per_state(state_id):
    """ get all place per state
    """
    all_places = set()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        for place in city.places:
            all_places.add(place)
    return all_places


def all_places_per_city(city_id):
    """ get all place per city
    """
    all_places = set()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        all_places.add(place)
    return all_places


@app_views.route('/places_search',
                 methods=['POST'],
                 strict_slashes=False)
def places_search():
    """ place search 
    """
    try:
        req = request.get_json(force=True)
    except Exception:
        abort(400, description="Not a JSON")
    all_places = set()
    states = req.get('states') or []
    cities = req.get('cities') or []
    if states is None or states == [] and cities is None or cities == []:
        all_states = storage.all(State)
        for state_id in all_states:
            res = all_places_per_state(state_id)
            all_places.update(res)
        all_places = [place.to_dict() for place in all_places]
        return jsonify(all_places)

    for state_id in states:
        res = all_places_per_state(state_id)
        all_places.update(res)

    for city_id in cities:
        res = all_places_per_city(city_id)
        all_places.update(res)

    all_places = [place.to_dict() for place in all_places]
    return jsonify(all_places)
