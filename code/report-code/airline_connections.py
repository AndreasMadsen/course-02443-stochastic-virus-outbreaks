""" Plots the airline connections """

import matplotlib.pyplot as plt

import _setup

from display import WorldMap
from world import regions, routes



base_map = WorldMap(resolution="c")

base_map.add_airports(regions)
base_map.add_airport_connections(regions)
base_map.save_fig("airport_connections.pdf")
