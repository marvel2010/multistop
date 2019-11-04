"""Utilities!"""


def filter_tradeoff(options):
    """Filters only the relevant tradeoffs."""
    options.sort()
    print("after sorting, before filtering", options)

    options_filtered = [options[0]]
    passenger_record = options[0][1]

    for option in options:
        if option[1] < passenger_record:
            options_filtered.append(option)
            passenger_record = option[1]

    print("after filtering", options_filtered)

    return options_filtered
