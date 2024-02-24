#!/usr/bin/python3
"""api"""
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, jsonify, make_response
app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """tears down the app whe the app closes"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles a 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    app.run(host=host if host else "0.0.0.0",
            port=port if port else 5000,
            threaded=True
            )
