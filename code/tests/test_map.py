import _setup
from display.world_map import WorldMap
from world import regions as region_module

#pickup regions
regions = iter(region_module.regions.values())

#plot them on a world mape
base_map = WorldMap()
base_map.add_regions(list(region_module.regions.values()))
base_map.show_plot()


