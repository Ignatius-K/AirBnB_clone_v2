#!/usr/bin/python3
"""Start Flask Application

Script starts a Flask Application
listening on 0.0.0.0:5000

Routes:
    - //cities_by_states: Displays cities with their states

Notes:
    - strict_slashes: set to False
"""
from flask import Flask, abort, jsonify, render_template
from models import storage
from models import amenity
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.route('/hbnb_filters')
def get_filtered_states():
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template(
        template_name_or_list='10-hbnb_filters.html',
        states=states,
        amenities=amenities
    )


@app.errorhandler(404)
def page_not_found(_):
    return render_template(
        template_name_or_list='404.html'
    ), 404


@app.teardown_appcontext
def clean_up(_):
    if storage is not None:
        storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
