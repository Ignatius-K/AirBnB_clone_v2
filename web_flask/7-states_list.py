#!/usr/bin/python3
"""Start Flask Application

Script starts a Flask Application
listening on 0.0.0.0:5000

Routes:
    - /states-list: Displays states

Notes:
    - strict_slashes: set to False
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def getStates():
    states = storage.all(State)
    return render_template(
        template_name_or_list='7-states_list.html',
        context=states
    )


@app.teardown_appcontext
def clean_up(response_or_exc):
    if storage is not None:
        storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
