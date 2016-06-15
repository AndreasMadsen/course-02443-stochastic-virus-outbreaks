import _setup
from display.world_map import WorldMap
from world import regions


# plot regions on a world mape
# base_map = WorldMap()
# base_map.add_regions(list(regions.values()))
# base_map.show_plot()

# plot regions on a world map
print(len(regions))
base_map = WorldMap(resolution="c")
base_map.add_voronoi(list(regions.values())[:])
base_map.show_plot()
