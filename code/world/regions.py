
import csv
import os.path as path
import textwrap

thisdir = path.dirname(path.realpath(__file__))
regions_csv = path.join(thisdir, '../../datasets/airport-population.csv')


class Region:
    def __init__(self, data):
        self.id = int(data['airport_id'])
        self.latitude = float(data['latitude'])
        self.longitude = float(data['longitude'])

        self.name = data['name']
        self.city = data['city']
        self.country = data['country']

        self.population = int(float(data['pop_sum']))
        self.neighbors = list(map(int, data['NEIGHBORS'].split(',')))
        self.airlines = []

    def __str__(self):
        return textwrap.dedent("""\
        Airport: {name} #{id}
        Place: {city} - {country} ({lat}, {long})
        population: {pop}
        airlines: {n_airlines}
        neighbors: {n_neighbors}
        """).format(
            id=self.id, name=self.name,
            city=self.city, country=self.country,
            lat=self.latitude, long=self.longitude,
            pop=self.population,
            n_airlines=len(self.airlines), n_neighbors=len(self.neighbors))

# dict mapping airport_id => Region()
regions = dict()

# Parse data and construct region objects
for region_raw in csv.DictReader(open(regions_csv), dialect='unix'):
    region = Region(region_raw)
    regions[region.id] = region

# Translate ids into region objects
for region in regions.values():
    region.neighbors = list(map(lambda neighbor_id: regions[neighbor_id], region.neighbors))
