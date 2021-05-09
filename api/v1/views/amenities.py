#!/usr/bin/python3
""" modules """
from flask import jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """ get all amenities instance state
    Returns:
        json: list of amenities instance
    """
    result = []
    for obj in storage.all(Amenity).values():
        result.append(obj.to_dict())
    return jsonify(result)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """ get amenity from the database using the storage instance
    Args:
        id (string): id of amenity instance
    Returns:
        json: in case instance doesn't exist we abord and the
        @app.errorhandler(HTTPException) in app.py file handle it
    """
    amenity = storage.get(Amenity, amenity_id)
    print(amenity)
    if amenity is None:
        return abort(404, description="Not Found")
    return amenity.to_dict()


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ we delete the instance corresponding on the id sent in the route
    Args:
        id (string): expect to be id of amenity instance
    Returns:
        json: if case instance doesn't exist we abord and the
        @app.errorhandler(HTTPException) in app.py file handle it
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return {}
    abort(404, description="Not Found")


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ create new amenity instance based on the json sent in the request
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

    if req.get('name') is None:
        abort(400, description='Missing name')
    new_amenity = Amenity(**req)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ route take as argument the amenity id, get
        the instance and update it
    Args:
        amenity_id (string): the amenity id we want to update
    Returns:
        json: dict of the instance
    """
    try:
        req = request.get_json(force=True)
    except Exception:
        abort(400, description="Not a JSON")

    obj_found = storage.get(Amenity, amenity_id)
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
