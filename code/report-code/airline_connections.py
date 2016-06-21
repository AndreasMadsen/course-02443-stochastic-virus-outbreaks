""" Plots the airline connections """

import matplotlib.pyplot as plt
import os.path as path

import _setup

from display import WorldMap
from world import regions, routes

this_dir = path.dirname(path.realpath(__file__))


base_map = WorldMap(resolution="c")

base_map.add_airports(regions)
base_map.add_airport_connections(regions)
base_map.save_fig(path.join(this_dir, '../../report/plots/airport_connections.pdf'))

