import _setup
from display.world_map import WorldMap
from world import regions


#plot regions on a world mape
base_map = WorldMap()
base_map.add_regions(list(regions.values()))
base_map.show_plot()

#plot regions on a world mape
base_map = WorldMap()
base_map.add_voronoi(list(regions.values())[::500])
base_map.show_plot()