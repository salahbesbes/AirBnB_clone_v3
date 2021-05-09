#!/usr/bin/python3
""" modules """
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review,
           "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """ Status of API """
    ok_status = {"status": "OK"}
    return jsonify(ok_status)


@app_views.route('/stats', strict_slashes=False)
def all_classes():
    """ get all cls
    """
    result = {}
    for key, cls in classes.items():
        result[key] = storage.count(cls)
    return jsonify(result)
