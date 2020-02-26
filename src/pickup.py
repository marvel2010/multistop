import os
import googlemaps
from datetime import datetime
from src.utils import response_to_matrix
from src.utils import filter_tradeoff
# import src.KEY
GOOGLE_MAPS_KEY = os.environ["GMAPS_API_KEY"]


def pickup(
        driver_start_location,
        passenger_start_location,
        end_location,
        stations,
        traffic_model_request,
        timing_model_request,
        departure_time_request,
        arrival_time_request
):
    """Calculates the total time spent by driver and passenger.

    Args:
        driver_start_location: string
        passenger_start_location: string
        end_location: string
        stations: the public transit stations to consider
        traffic_model_request: "best_guess", "optimistic", or "pessimistic"
        timing_model_request: "leaving_now", "depart_at", or "arrive_by"
        departure_time_request: iso format, approximate time of departure
        arrival_time_request: iso format, approximate time of arrival

    Returns:
        options: (driver_time, passenger_time, pickup_station, shared_leg_time)
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

    response_1_driver = gmaps.distance_matrix(
        driver_start_location,
        [station[1] for station in stations],
        mode="driving",
        departure_time=departure_time,
        arrival_time=arrival_time,
        traffic_model=traffic_model,
    )

    response_1_passenger = gmaps.distance_matrix(
        passenger_start_location,
        [station[1] for station in stations],
        mode="transit",
        departure_time=departure_time,
        arrival_time=arrival_time,
    )

    response_2 = gmaps.distance_matrix(
        [station[1] for station in stations],
        end_location,
        mode="driving",
        departure_time=departure_time,
        arrival_time=arrival_time,
        traffic_model=traffic_model,
    )

    # traffic information is only used when the departure time is specified
    if timing_model_request == "arrive_by":
        matrix_1_driver = response_to_matrix(response_1_driver, "duration")
        matrix_1_passenger = response_to_matrix(response_1_passenger, "duration")
        matrix_2 = response_to_matrix(response_2, "duration")
    else:
        matrix_1_driver = response_to_matrix(response_1_driver, "duration_in_traffic")
        matrix_1_passenger = response_to_matrix(response_1_passenger, "duration")
        matrix_2 = response_to_matrix(response_2, "duration_in_traffic")

    options = [
        (
            matrix_1_driver[0][i] + matrix_2[i][0],
            matrix_1_passenger[0][i] + matrix_2[i][0],
            station[0],
            matrix_2[i][0]
        )
        for i, station in enumerate(stations)
    ]

    filtered_options = filter_tradeoff(options)

    return filtered_options
