#!/usr/bin/python3
""" modules """
from flask import jsonify, abort, request
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', strict_slashes=False)
def users():
    """ get all State instance from the database
    Returns:
        json: list of State instance
    """
    result = []
    for obj in storage.all(User).values():
        result.append(obj.to_dict())
    return jsonify(result)
