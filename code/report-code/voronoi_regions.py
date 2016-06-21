""" Plots the voronoi regions"""
import _setup

import os.path as path
from display import WorldMap
from simulator import State
from world import regions, routes

import matplotlib.pyplot as plt

this_dir = path.dirname(path.realpath(__file__))

# plot regions on a world map
base_map = WorldMap(resolution="l")
base_map.add_airports(regions)
base_map.add_voronoi(regions)
#base_map.show()
plt.savefig(path.join(this_dir, '../../report/plots/voronoi.pdf'),
            format='pdf', dpi=1000, bbox_inches='tight')
