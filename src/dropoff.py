import os
import googlemaps
from datetime import datetime
from datetime import timedelta
from src.stations import BART_STATIONS
from src.utils import response_to_matrix
from src.utils import filter_tradeoff
# import src.KEY
GOOGLE_MAPS_KEY = os.environ["GMAPS_API_KEY"]


def dropoff(
        start_location,
        driver_end_location,
        passenger_end_location,
        traffic_model_request,
        timing_model_request,
        departure_time_request,
        arrival_time_request
):
    """Calculates the total time spent by driver and passenger.

    Args:
        start_location: string
        driver_end_location: string
        passenger_end_location: string
        traffic_model_request: "best_guess", "optimistic", or "pessimistic"
        timing_model_request: "leaving_now", "depart_at", or "arrive_by"
        departure_time_request: iso format, approximate time of departure
        arrival_time_request: iso format, approximate time of arrival

    Returns:
        options: (driver_time, passenger_time, dropoff_station, shared_leg_time)
    """

    gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)
    assert traffic_model_request in ["best_guess", "optimistic", "pessimistic"], "invalid traffic model"
    assert timing_model_request in ["leaving_now", "depart_at", "arrive_by"], "invalid timing model"

    # set departure time or arrival time, but not both
    if timing_model_request == "leaving_now":
        departure_time, arrival_time = datetime.now(), None
        traffic_model = traffic_model_request
    elif timing_model_request == "depart_at":
        departure_time, arrival_time = datetime.fromisoformat(departure_time_request), None
        traffic_model = traffic_model_request
    elif timing_model_request == "arrive_by":
        departure_time, arrival_time = None, datetime.fromisoformat(arrival_time_request)
        traffic_model = None
    else:
        raise ValueError("Unrecognized timing model.")

    response_1 = gmaps.distance_matrix(
        start_location,
        BART_STATIONS,
        mode="driving",
        departure_time=departure_time,
        arrival_time=arrival_time,
        traffic_model=traffic_model,
    )

    response_2_driver = gmaps.distance_matrix(
        BART_STATIONS,
        driver_end_location,
        mode="driving",
        departure_time=departure_time,
        arrival_time=arrival_time,
        traffic_model=traffic_model,
    )

    response_2_passenger = gmaps.distance_matrix(
        BART_STATIONS,
        passenger_end_location,
        mode="transit",
        departure_time=departure_time,
        arrival_time=arrival_time,
    )

    # traffic information is only used when the departure time is specified
    if timing_model_request == "arrive_by":
        matrix_1 = response_to_matrix(response_1, "duration")
        matrix_2_driver = response_to_matrix(response_2_driver, "duration")
        matrix_2_passenger = response_to_matrix(response_2_passenger, "duration")
    else:
        matrix_1 = response_to_matrix(response_1, "duration_in_traffic")
        matrix_2_driver = response_to_matrix(response_2_driver, "duration_in_traffic")
        matrix_2_passenger = response_to_matrix(response_2_passenger, "duration")

    options = [
        (
            matrix_1[0][i] + matrix_2_driver[i][0],
            matrix_1[0][i] + matrix_2_passenger[i][0],
            bart_station,
            matrix_1[0][i]
        )
        for i, bart_station in enumerate(BART_STATIONS)
    ]

    filtered_options = filter_tradeoff(options)

    if departure_time is not None:
        for i, filtered_option in enumerate(filtered_options):
            passenger_transit_time_with_wait = _transit_time_with_wait(
                start_time=departure_time + timedelta(seconds=filtered_option[3]),
                start_location=filtered_option[2],
                end_location=passenger_end_location,
            )
            filtered_options[i] = (
                filtered_option[0],
                filtered_option[3] + passenger_transit_time_with_wait,
                filtered_option[2],
                filtered_option[3]
            )

    return filtered_options


def _transit_time_with_wait(
        start_time,
        start_location,
        end_location
):
    """Calculates the total time spent by a transit passenger, including wait time.

    Args:
        start_time: datetime object
        start_location: string
        end_location: string

    Returns:
        passenger_time
    """
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)
    response = gmaps.directions(
        start_location,
        end_location,
        mode="transit",
        departure_time=start_time
    )

    if "arrival_time" in response[0]["legs"][0].keys():
        end_time = datetime.fromtimestamp(response[0]["legs"][0]["arrival_time"]["value"])
        time_with_wait = (end_time - start_time) // timedelta(seconds=1)
        return time_with_wait
    else:
        return response[0]["legs"][0]["duration"]["value"]
