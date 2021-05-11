#!/usr/bin/python3
"""holds places reviews"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    all_reviews = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        all_reviews.append(review.to_dict())
    return (jsonify(all_reviews))


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review_to_get = storage.get(Review, review_id)
    if review_to_get is None:
        abort(404)
    return jsonify(review_to_get.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review_to_delete = storage.get(Review, review_id)
    if review_to_delete is None:
        abort(404)
    review_to_delete.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    review_to_post = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if review_to_post is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    user_id = review_to_post.get("user_id")
    if user_id is None:
        return (jsonify({"error": "Missing user_id"}), 400)
    user_found = storage.get(User, review_to_post['user_id'])
    if user_found is None:
        abort(404)
    review_text = review_to_post.get("text")
    if review_text is None:
        return (jsonify({"error": "Missing text"}), 400)
    new = Review(**review_to_post)
    storage.new(new)
    storage.save()
    return (jsonify(new), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object"""
    old_review = storage.get(Review, review_id)
    if old_review is None:
        abort(404)
    req_body = request.get_json()
    if req_body is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    to_ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in req_body.items():
        if key not in to_ignore:
            setattr(old_review, key, value)

    old_review.save()
    storage.save()
    return (jsonify(old_review.to_dict()), 200)
