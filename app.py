import sys
import logging
from flask import Flask, render_template, request
from src.dropoff import dropoff as dropoff_fn
from src.pickup import pickup as pickup_fn
from src.stations import STATIONS_MAP
from src.stations import TIMEZONES_MAP
from src.stations import SYSTEM_NAMES_MAP

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dropoff", methods=["GET", "POST"])
def dropoff():
    if request.method == "POST":
        logging.info("dropoff:%s" % request.form)
        start = request.form["loc-1"]
        driver_end = request.form["loc-2"]
        passenger_end = request.form["loc-3"]
        traffic_model = request.form["traffic-model"]
        timing_model = request.form["timing-model"]
        departure_time = request.form["depart-at-time"]
        arrival_time = request.form["arrive-by-time"]
        options = dropoff_fn(
            start,
            driver_end,
            passenger_end,
            stations=STATIONS_MAP[request.form["city"]],
            departure_time_request=departure_time,
            arrival_time_request=arrival_time,
            traffic_model_request=traffic_model,
            timing_model_request=timing_model,
            tzone=TIMEZONES_MAP[request.form["city"]]
        )
        return render_template(
            "output.html",
            options=options,
            transit_system=SYSTEM_NAMES_MAP[request.form["city"]],
            loc_1_name="Mutual Start Location",
            loc_1_value=start,
            loc_2_name="Driver End Location",
            loc_2_value=driver_end,
            loc_3_name="Passenger End Location",
            loc_3_value=passenger_end,
            stop_name="Dropoff Stop"
        )

    return render_template(
        "input.html",
        loc_1_name="Mutual Start Location",
        loc_2_name="Driver End Location",
        loc_3_name="Passenger End Location",
        img_path="Dropoff.png"
    )


@app.route("/pickup", methods=["GET", "POST"])
def pickup():
    if request.method == "POST":
        logging.info("pickup:%s" % request.form)
        driver_start = request.form["loc-1"]
        passenger_start = request.form["loc-2"]
        end = request.form["loc-3"]
        traffic_model = request.form["traffic-model"]
        timing_model = request.form["timing-model"]
        departure_time = request.form["depart-at-time"]
        arrival_time = request.form["arrive-by-time"]
        options = pickup_fn(
            driver_start,
            passenger_start,
            end,
            stations=STATIONS_MAP[request.form["city"]],
            departure_time_request=departure_time,
            arrival_time_request=arrival_time,
            traffic_model_request=traffic_model,
            timing_model_request=timing_model,
            tzone=TIMEZONES_MAP[request.form["city"]]
        )
        return render_template(
            "output.html",
            options=options,
            transit_system=SYSTEM_NAMES_MAP[request.form["city"]],
            loc_1_name="Driver Start Location",
            loc_1_value=driver_start,
            loc_2_name="Passenger Start Location",
            loc_2_value=passenger_start,
            loc_3_name="Mutual End Location",
            loc_3_value=end,
            stop_name="Pickup Stop"
        )

    return render_template(
        "input.html",
        loc_1_name="Driver Start Location",
        loc_2_name="Passenger Start Location",
        loc_3_name="Mutual End Location",
        img_path="Pickup.png"
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        app.run(debug=True)
    else:
        app.run(debug=False)
