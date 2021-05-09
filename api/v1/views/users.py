#!/usr/bin/python3
""" modules """
from flask import abort, request
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import abort


@app_views.route('/users', strict_slashes=False)
def users():
    """ get all State instance from the database
    Returns:
        json: list of State instance
    """
    result = []
    for obj in storage.all(User).values():
        result.append(obj.to_dict())
    return (jsonify(result))

@get.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def get():
    """ Retrieves the list of all User objects """
    result = storage.get(User, user_id)
    if result is None:
        abort(404)
    return (jsonify(result.to_dict()))

@delete.route('/users/<string:user_id>', method=['GET', 'DELETE'], strict_slashes=False)
def delete():
    """Delete a User object"""
    result = storage.get(User, user_id)
    if result is None:
        abort(404)
    storage.delete()
    storage.save()
    return (jsonify({}), 200)

@create.route('/users/<string:user_id>', method=['POST'], strict_slashes=False)
def post():
    """Creates a User object """
    if request.get_json() is None:
        return (jsonify({'error' : 'Not a JSON'}), 400)
    mail = 0
    pwd = 0
    for key in request.get_json().keys():
        if key == 'email':
            mail += 1
        if key == 'password'
            pwd += 1
    if mail < 1:
        return (jsonify({'error': 'Missing email'}), 400)
    if pwd < 1:
        return (jsonify({'error': 'Missing password'}), 400)
    new = User(email=request.get_json(['email']), 
               password=request.get_json(['password'])
    new.save()
    return (jsonify(new.to_dict()), 201)

@update.route('/users/<string:user_id>', method['PUT', 'GET'], strict_slashes=False)
def put()
    """Updates a User object"""
    result = storage.get(User, user_id) 
    if result is None:
        abort(404)
    else:
        if request.get_json is None:
            return (jsonify({'error' : 'not JSON'}), 404)
        to_ignore['id', 'email', 'created_at', 'updated_at']
        for key, value in request.get_json().items:
            if key not in to_ignore:
                setattr(User, key, value)
        User.save()
        return (jsonify(user.to_dict()), 200) 