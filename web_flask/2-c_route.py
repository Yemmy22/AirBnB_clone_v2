#!/usr/bin/python3
'''
This script starts a flask web application and executes it on port 5000
'''
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def start_web_app():
    return "Hello HBNB!"


@app.route('/hbnb')
def slash_hbnb():
    return "HBNB"


@app.route('/c/<text>')
def c_slash_text(text):
    if text:
        if '_' in text:
            text = text.replace('_', ' ')
        return f'C ' + text


if __name__ == "__main__":
    app.run(debug=True, port=5000)
