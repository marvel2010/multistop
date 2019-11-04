import os
import googlemaps
from datetime import datetime
from src.stations import BART_STATIONS
from src.utils import response_to_matrix
# import src.KEY
GOOGLE_MAPS_KEY = os.environ["GMAPS_API_KEY"]


def pickup(driver_start_location, passenger_start_location, end_location):
    """Calculates the total time spent by driver and passenger.

    Args:
        driver_start_location: string
        passenger_start_location: string
        end_location: string

    Returns:
        options: (driver_time, passenger_time, pickup_station)
    """

    gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)
    now = datetime.now()

    response_1_driver = gmaps.distance_matrix(
        driver_start_location, BART_STATIONS, mode="driving", departure_time=now
    )
    response_1_passenger = gmaps.distance_matrix(
        passenger_start_location, BART_STATIONS, mode="transit", departure_time=now
    )
    response_2 = gmaps.distance_matrix(
        BART_STATIONS, end_location, mode="driving", departure_time=now
    )

    matrix_1_driver = response_to_matrix(response_1_driver)
    matrix_1_passenger = response_to_matrix(response_1_passenger)
    matrix_2 = response_to_matrix(response_2)

    options = [
        (
            matrix_1_driver[0][i] + matrix_2[i][0],
            matrix_1_passenger[0][i] + matrix_2[i][0],
            bart_station,
        )
        for i, bart_station in enumerate(BART_STATIONS)
    ]

    return options
