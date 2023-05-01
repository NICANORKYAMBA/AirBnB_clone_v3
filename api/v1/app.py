#!/usr/bin/python3
"""
//
"""
from api.v1.views import app_views
from flask import Blueprint
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
CORS(app, origins='0.0.0.0')
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(td):
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Handles 404 errors"""
    response = jsonify({'error': 'Not found'})
    response.status_code = 404

    return response


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = HBNB_API_HOST if HBNB_API_HOST else "0.0.0.0"
    port = HBNB_API_PORT if HBNB_API_PORT else 5000

    app.run(host, port, threaded=True)
