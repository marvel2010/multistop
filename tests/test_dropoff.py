import pytest
import googlemaps
from src.dropoff import dropoff as dropoff_fn
from src.stations import BART_STATIONS, LINK_STATIONS
from tests.utils import OAK, SFO, SJC, SEA, BFI, PAE
from tests.utils import TOMORROW, YESTERDAY

good_dropoffs = [
    ("best_guess", "leaving_now", None, None),
    ("optimistic", "leaving_now", None, None),
    ("pessimistic", "leaving_now", None, None),
    ("best_guess", "depart_at", TOMORROW, None),
    ("best_guess", "arrive_by", None, TOMORROW),
]


@pytest.mark.parametrize("traffic_model,timing_model,departure_time,arrival_time", good_dropoffs)
def test_good_bart_dropoffs(traffic_model, timing_model, departure_time, arrival_time):
    options = dropoff_fn(
        start_location=SJC,
        passenger_end_location=SFO,
        driver_end_location=SJC,
        stations=BART_STATIONS,
        traffic_model_request=traffic_model,
        timing_model_request=timing_model,
        departure_time_request=departure_time,
        arrival_time_request=arrival_time,
        tzone="America/Los_Angeles"
    )
    assert len(options)


@pytest.mark.parametrize("traffic_model,timing_model,departure_time,arrival_time", good_dropoffs)
def test_good_link_pickups(traffic_model, timing_model, departure_time, arrival_time):
    options = dropoff_fn(
        start_location=PAE,
        passenger_end_location=SEA,
        driver_end_location=PAE,
        stations=LINK_STATIONS,
        traffic_model_request=traffic_model,
        timing_model_request=timing_model,
        departure_time_request=departure_time,
        arrival_time_request=arrival_time,
        tzone="America/Los_Angeles"
    )
    assert len(options)


def test_timing_error():
    with pytest.raises(googlemaps.exceptions.ApiError):
        dropoff_fn(
            start_location=SEA,
            passenger_end_location=BFI,
            driver_end_location=PAE,
            stations=LINK_STATIONS,
            traffic_model_request="best_guess",
            timing_model_request="depart_at",
            departure_time_request=YESTERDAY,
            arrival_time_request=None,
            tzone="America/Los_Angeles"
        )
