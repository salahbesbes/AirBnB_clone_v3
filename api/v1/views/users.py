#!/usr/bin/python3
""" modules """
from flask import abort, request
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify


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
        abort (404)
    return (jsonify(result.to_dict()))

@delete.route('/users/<string:user_id>', method=['GET', 'DELETE'], strict_slashes=False)
def delete():
    """Delete a User object"""
    result = storage.get(User, user_id)
    if result is None:
        abort (404)
    storage.delete()
    storage.save()
    return (jsonify({}), 200)

@create.route('/users/<string:user_id>', method=['POST'])
def post():
    """transform the HTTP body request in json format 
    to a dictionary containing the items email and password
    """
    if request.get_json() is None:
        return (jsonify({'error' : 'Not a JSON', 400)
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

@put.route()