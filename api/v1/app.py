#!/usr/bin/python3
""" modules """
from os import getenv
from flask import Flask
from flask import jsonify
from werkzeug.exceptions import HTTPException
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_404(error):
    """ Return a custom 404 error """
    err_dict = {"error": "Not found"}
    return jsonify(err_dict), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default='5000')
    app.run(port=port, host=host, threaded=True)
