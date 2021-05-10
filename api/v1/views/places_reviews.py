#!/usr/bin/python
"""holds places reviews"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('places/<place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    all_reviews=[]
    place = storage.get("Place", place_id)
    if place is None:
        abort (404)
    for review in place.reviews:
        all_reviews.append(review.dict())
    return (jsonify(all_reviews))

@app_views.route('reviews/<review_id>', methods=['GET'],
                  strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review_to_get = storage.get(Review, review_id)
    if review_to_get is None:
        abort (404)
    return jsonify(review_to_get.dict())

@app_views.route('reviews/<review_id>', methods=['DELETE'],
                  strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review_to_delete = storage.get(Review, review_id)
    if review_to_delete is None:
        abort (404)
    review_to_delete.delete()
    storage.save()
    return jsonify('{}'), 200

@app_views.route('places/<place_id>/reviews', method=['POST'],
                  strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    review_to_post = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort (404)
    if review_to_post is None :
        return (jsonify({"error" : "Not a JSON"}), 400)
    user_id = review_to_post.get("user_id")
    if user_id is None:
        return (jsonify({"error" : "Missing user_id"}), 400)
    id_found = storage.get("user_id", review_to_post['user_id']) 
    if id_found is None:
        abort(404)
    review_text = review_to_post.get("text")
    if review_text is None :
        return (jsonify({'error': 'Missing text'}), 400)
    new = Review(place_id=place, user_id=user_id, text=review_text)
    return (jsonify(new.to_dict()), 201)

