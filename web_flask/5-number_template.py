#!/usr/bin/python3
'''
This script starts a flask web application and executes it on port 5000
'''
from flask import Flask, render_template
from markupsafe import escape

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


@app.route('/python', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def redirect_python(text):
    if text:
        if '_' in text:
            text = text.replace('_', ' ')
    return f"Python {escape(text)}"


@app.route('/number/<int:n>')
def number_slash_int(n):
    return f'{n} is a number'


@app.route('/number_template/<int:n>')
def slash_number_template(n):
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
