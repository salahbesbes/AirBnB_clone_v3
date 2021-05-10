#!/usr/bin/python3
""" modules """
from os import getenv
from flask import Flask
from flask.json import jsonify
from werkzeug.exceptions import HTTPException
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    if e.code == 400:
        return jsonify({"error": e.description}), 400


@app.errorhandler(404)
def handle_404(e):
    """ handle 404 exception"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(HTTPException)
def handle_404(e):
    """ handle 404 exception"""
    return jsonify({"error": e.description}), 404

if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default='5000')
    app.run(port=port, host=host, threaded=True, debug=True)
