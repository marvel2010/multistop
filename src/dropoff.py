import os
import googlemaps
from datetime import datetime
from src.stations import BART_STATIONS
GOOGLE_MAPS_KEY = os.environ["GMAPS_API_KEY"]


def dropoff(start_location, driver_end_location, passenger_end_location):
    """Calculates the total time spent by driver and passenger.

    Args:
        start_location: string
        driver_end_location: string
        passenger_end_location: string

    Returns:
        options: (driver_time, passenger_time, dropoff_station)
    """

    gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)
    now = datetime.now()

    response_1 = gmaps.distance_matrix(
        start_location, BART_STATIONS, mode="driving", departure_time=now
    )
    response_2_driver = gmaps.distance_matrix(
        BART_STATIONS, driver_end_location, mode="driving", departure_time=now
    )
    response_2_passenger = gmaps.distance_matrix(
        BART_STATIONS, passenger_end_location, mode="transit", departure_time=now
    )

    matrix_1 = _response_to_matrix(response_1)
    matrix_2_driver = _response_to_matrix(response_2_driver)
    matrix_2_passenger = _response_to_matrix(response_2_passenger)

    options = [
        (
            matrix_1[0][i] + matrix_2_driver[i][0],
            matrix_1[0][i] + matrix_2_passenger[i][0],
            bart_station,
        )
        for i, bart_station in enumerate(BART_STATIONS)
    ]

    return options


def _response_to_matrix(response):
    matrix = []
    for row in response["rows"]:
        matrix.append([element["duration"]["value"] for element in row["elements"]])
    return matrix
