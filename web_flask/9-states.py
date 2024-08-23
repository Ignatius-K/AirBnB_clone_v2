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
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=True)
def get_states():
    states = storage.all(State)
    return render_template(
        template_name_or_list='9-states.html',
        states=states
    )


@app.route('/states/<uuid:id>')
def get_state(id):
    states = storage.all(State)
    state = states.get(f'State.{id}')
    if state is None:
        abort(404)
    return render_template(
        template_name_or_list='9-states.html',
        state=state
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
