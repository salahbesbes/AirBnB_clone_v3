#!/usr/bin/python3
""" modules """
from models.place import Place
from flask import abort
from models.place import Place
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask.json import jsonify


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def amenities_of_place(place_id):
    """ get all amenities instance from place
    Returns:
        json: list of amenities instance in the place found
    """
    result = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Not Found")
    for obj in place.amenities:
        result.append(obj.to_dict())

    return jsonify(result)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """ delete amenity from the place instace
    Args:
        amenity_id (string): id of amenity instance
        place_id (string): id of place instance
    Returns:
        json: in case instance doesn't exist we abord and the
        @app.errorhandler(HTTPException) in app.py file handle it
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Not Found")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, description="Not Found")
    if amenity in place.amenities:
        amenity.delete()
        storage.save()
        return {}
    abort(404, description="Not Found")


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity_place(place_id, amenity_id):
    """ create amenity - place relation
    Args:
        amenity_id (string): id of amenity instance
        place_id (string): id of place instance
    Returns:
        json: Amenity instance, in case instance doesn't exist we abord and the
        @app.errorhandler(HTTPException) in app.py file handle it
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Not Found")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, description="Not Found")

    if amenity in place.amenities:
        return jsonify(amenity.to_dict())

    place.amenities.append(amenity)
    storage.new(place)
    storage.save()
    return jsonify(amenity.to_dict())
