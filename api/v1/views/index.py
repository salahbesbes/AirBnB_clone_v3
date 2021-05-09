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


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review,
           "State": State, "User": User}


@app_views.route('/status', strict_slashes=False)
def status():
    result = {}
    for key, cls in classes.items():
        result[key] = len(storage.all(cls))
    return jsonify(result)
