from flask import Flask, render_template, request
import googlemaps
import time
import os

# gmaps = googlemaps.Client(key=None)

app = Flask(__name__)


@app.route('/')
def index(user=None):
    return render_template('index.html', usrname=user)


if __name__ == '__main__':
    app.run(debug=True)
