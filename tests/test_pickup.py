import pytest
import googlemaps
from datetime import datetime, timedelta
from src.pickup import pickup as pickup_fn
from src.stations import BART_STATIONS, LINK_STATIONS
from tests.utils import OAK, SFO, SJC, SEA, BFI, PAE
from tests.utils import TOMORROW, YESTERDAY

good_pickups = [
    ("best_guess", "leaving_now", None, None),
    ("optimistic", "leaving_now", None, None),
    ("pessimistic", "leaving_now", None, None),
    ("best_guess", "depart_at", TOMORROW, None),
    ("best_guess", "arrive_by", None, TOMORROW),
]


@pytest.mark.parametrize("traffic_model,timing_model,departure_time,arrival_time", good_pickups)
def test_good_bart_pickups(traffic_model, timing_model, departure_time, arrival_time):
    options = pickup_fn(
        driver_start_location=OAK,
        passenger_start_location=SFO,
        end_location=SJC,
        stations=BART_STATIONS,
        traffic_model_request=traffic_model,
        timing_model_request=timing_model,
        departure_time_request=departure_time,
        arrival_time_request=arrival_time,
        tzone="America/Los_Angeles"
    )
    assert len(options)
    assert options[0][0] > 20


@pytest.mark.parametrize("traffic_model,timing_model,departure_time,arrival_time", good_pickups)
def test_good_link_pickups(traffic_model, timing_model, departure_time, arrival_time):
    options = pickup_fn(
        driver_start_location=SEA,
        passenger_start_location=BFI,
        end_location=PAE,
        stations=LINK_STATIONS,
        traffic_model_request=traffic_model,
        timing_model_request=timing_model,
        departure_time_request=departure_time,
        arrival_time_request=arrival_time,
        tzone="America/Los_Angeles"
    )
    assert len(options)
    assert options[0][0] > 20


def test_timing_error():
    with pytest.raises(googlemaps.exceptions.ApiError):
        pickup_fn(
            driver_start_location=SEA,
            passenger_start_location=BFI,
            end_location=PAE,
            stations=LINK_STATIONS,
            traffic_model_request="best_guess",
            timing_model_request="depart_at",
            departure_time_request=YESTERDAY,
            arrival_time_request=None,
            tzone="America/Los_Angeles"
        )
