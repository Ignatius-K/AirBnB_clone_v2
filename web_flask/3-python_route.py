#!/usr/bin/python3
"""Start Flask Application

Script starts a Flask Application
listening on 0.0.0.0:5000

Routes:
    - /
    - /hbnb: Courtesy for Holberton school of Magic
    - /c: Courtesy for C being cool
    - /python: Courtesy for Python being awesome

Notes:
    - strict_slashes: set to False
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    '''Index route'''
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    '''HBNB route'''
    return 'HBNB'


@app.route('/c/<string:text>', strict_slashes=False)
def c_route(text: str):
    '''C route'''
    return f'C {text.replace("_", " ")}'


@app.route('/python', strict_slashes=False)
@app.route('/python/<string:text>', strict_slashes=False)
def python_route(text: str = 'is cool'):
    '''Python route'''
    return f'Python {text.replace("_", " ")}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
