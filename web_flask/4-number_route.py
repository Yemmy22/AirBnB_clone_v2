#!/usr/bin/python3
'''
This script starts a flask web application and executes it on port 5000
'''
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def start_web_app():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def slash_hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_slash_text(text):
    if text:
        if '_' in text:
            text = text.replace('_', ' ')
        return f'C ' + text


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def redirect_python(text):
    if text:
        if '_' in text:
            text = text.replace('_', ' ')
    return f"Python {escape(text)}"


@app.route('/number/<int:n>', strict_slashes=False)
def number_slash_int(n):
    return f'{n} is a number'

if __name__ == "__main__":
    app.run(debug=True, port=5000)
