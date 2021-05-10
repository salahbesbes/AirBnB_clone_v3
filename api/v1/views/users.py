#!/usr/bin/python3
""" modules """
from flask import abort, request
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify
from hashlib import md5


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


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves the list of all User objects """
    result = storage.get(User, user_id)
    if result is None:
        abort(404)
    return (jsonify(result.to_dict()))


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a User object"""
    result = storage.get(User, user_id)
    if result is None:
        abort(404)

    storage.delete(result)
    storage.save()
    return ({}, 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object """
    req = request.get_json()
    if req is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    email = req.get('email')
    if email is None:
        return (jsonify({'error': 'Missing email'}), 400)
    password = req.get('password')
    if password is None:
        return (jsonify({'error': 'Missing password'}), 400)
    exclude = ['id', 'created_at', 'updated_at']
    all_atributes_user_add = {k: v for k, v in req.items() if k not in exclude}
    new = User(**all_atributes_user_add)
    new.save()
    storage.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user_found = storage.get(User, user_id)
    if user_found is None:
        abort(404)
    else:
        req = request.get_json()
        if req is None:
            return (jsonify({'error': 'Not JSON'}), 400)

        to_ignore = ['id', 'email', 'created_at', 'updated_at']
        for key, value in req.items():
            if key not in to_ignore:
                if key == 'password':
                    value = md5(value.encode('utf8')).hexdigest()
                setattr(user_found, key, value)
        user_found.save()
        storage.save()
        return (jsonify(user_found.to_dict()), 200)
