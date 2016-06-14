
def cross_reference(regions, routes):
    for route in routes.values():
        if route.source_id not in regions or route.destination_id not in regions:
            continue

        route.source = regions[route.source_id]
        route.destination = regions[route.destination_id]

        route.source.airlines.append(route)
