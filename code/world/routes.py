
import csv
import os.path as path
import textwrap

thisdir = path.dirname(path.realpath(__file__))
routes_csv = path.join(thisdir, '../../datasets/airport-routes.csv')

def parse_airport_id(id_str):
    if id_str == '\\N':
        return None
    else:
        return int(id_str)

class Route:
    def __init__(self, data):
        """Holds information about a route

        The attributes are:

        airline_ids: list of all airline ids on this route
        source: route source as a Region object
        destination: route destination as a Region object

        count: number of airlines on this route
        """
        self.airline_ids = [parse_airport_id(data['airline_id'])]

        self.source_id = parse_airport_id(data['source_airport_id'])
        self.source = None
        self.destination_id = parse_airport_id(data['destination_airport_id'])
        self.destination = None

        self.count = 1

    @property
    def route_id(self):
        return (self.source_id, self.destination_id)

    @property
    def real_route(self):
        return self.source_id is not None and self.destination_id is not None

    def add_route(self, route):
        self.airline_ids += route.airline_ids
        self.count += route.count

# dict mapping (from_airport_id, to_airport_id) => Route()
routes = dict()

# Parse data and construct region objects
for routes_raw in csv.DictReader(open(routes_csv), dialect='unix'):
    route = Route(routes_raw)
    if not route.real_route: continue

    if route.route_id in routes:
        routes[route.route_id].add_route(route)
    else:
        routes[route.route_id] = route
