"""Utilities!"""
import numpy as np
import logging


def response_to_matrix(response, field):
    """Converts distance_matrix API response to a 2d matrix."""
    logging.debug("response_to_matrix : %s : %s" % (field, response))
    matrix = []
    for row in response["rows"]:
        matrix.append([element.get(field, {"value": np.Infinity})["value"] for element in row["elements"]])
    return matrix


def filter_tradeoff(options):
    """Filters only the relevant tradeoffs."""
    options.sort()

    options_filtered = [options[0]]
    passenger_record = options[0][1]

    for option in options:
        if option[1] < passenger_record:
            options_filtered.append(option)
            passenger_record = option[1]

    return options_filtered
