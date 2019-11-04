import sys
from flask import Flask, render_template, request
from src.dropoff import dropoff as dropoff_fn
from src.utils import filter_tradeoff

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dropoff", methods=["GET", "POST"])
def dropoff():
    if request.method == "POST":
        start = request.form["start"]
        driver_end = request.form["driver-end"]
        passenger_end = request.form["passenger-end"]
        options = dropoff_fn(start, driver_end, passenger_end)
        options_filtered = filter_tradeoff(options)
        return render_template("dropoff_out.html", options=options_filtered)

    return render_template("dropoff_in.html")


@app.route("/pickup", methods=["GET", "POST"])
def pickup():
    if request.method == "POST":
        return None

    return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        app.run(debug=True)
    else:
        app.run(debug=False)
