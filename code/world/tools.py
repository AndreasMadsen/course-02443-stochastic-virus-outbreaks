
from .regions import regions

def airline_connections(region):
    """Find indgoing and outgoing airline connections

    Parameters
    ---------
    region : Region object to check for ingoing and outgoing connections

    Returns
    -------
    (outgoing, ingoing) route objects
    """

    outgoing_routes = region.airlines
    ingoing_routes = []

    for other_region in regions.values():
        if other_region == region: continue

        for airline in other_region.airlines:
            if airline.destination == region:
                ingoing_routes.append(airline)

    return (outgoing_routes, ingoing_routes)
