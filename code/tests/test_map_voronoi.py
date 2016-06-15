import _setup

from display import WorldMap
from simulator import State
from world import regions, routes

# plot regions on a world map
base_map = WorldMap(resolution="c")
base_map.add_airports(regions)
base_map.add_voronoi(regions)
base_map.show()
