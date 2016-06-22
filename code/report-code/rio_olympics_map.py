import _setup

import os.path as path
import time

from display import WorldMap
from simulator import State, Simulator
from world import regions, routes

this_dir = path.dirname(path.realpath(__file__))

len_simulation = 90

state = State(regions, routes, verbose=True)
state.set_outbreak('Rio De Janeiro', 1000)

sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5, verbose=True,)
sim.add_event(2560, days=18, total_transfer=380e3)
base_map = WorldMap(resolution="c")
base_map.animate(sim, frames=len_simulation, max_infected=0.1)
base_map.ani.save(path.join(this_dir, '../../report/plots/gifs/rio.gif'),
    writer="imagemagick", fps=3)


state = State(regions, routes, verbose=True)
state.set_outbreak('Rio De Janeiro', 1000)
sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5, verbose=True)
base_map = WorldMap(resolution="c")
base_map.animate(sim, frames=len_simulation, max_infected=0.1)
base_map.ani.save(path.join(this_dir, '../../report/plots/gifs/no_rio.gif'),
    writer="imagemagick", fps=3)
