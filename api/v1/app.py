#!/usr/bin/python3
""" modules """
from os import getenv
from flask import Flask
from flask.json import jsonify
# from werkzeug.exceptions import HTTPException
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
# CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # TODO: explore the e Exception methods
    # this methode get called when ever abort() is called
    # return jsonify({
    #     "code": e.code,
    #     "name": e.name,
    #     "description": e.description,
    # })
    # if e.code == 404:
    #     return jsonify({"error": "Not Found"})
    return jsonify({"error": e.description})


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default='5000')
    app.run(port=port, host=host)
