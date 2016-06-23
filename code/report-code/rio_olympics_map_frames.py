import _setup

import os.path as path
import time

from display import WorldMap
from simulator import State, Simulator
from world import regions, routes

this_dir = path.dirname(path.realpath(__file__))

len_simulation = 67

state = State(regions, routes, verbose=True)
state.set_outbreak('Rio De Janeiro', 1000)

sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5, verbose=True,)
sim.add_event(2560, days=18, total_transfer=380e3)

for i, state in enumerate(sim.run(len_simulation)):
    fig_name = path.join(this_dir, '../../report/plots/gifs/frames/rio-{0}.pdf'.format(i))
    if i == 46:
        base_map = WorldMap(resolution="c")
        base_map.scatter_infections(state, max_infected=0.1, time=i)
        base_map.save_fig(fig_name)
        break


state = State(regions, routes, verbose=True)
state.set_outbreak('Rio De Janeiro', 1000)
sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5, verbose=True)

for i, state in enumerate(sim.run(len_simulation)):
    fig_name = path.join(this_dir, '../../report/plots/gifs/frames/noRio-{0}.pdf'.format(i))
    if i == 67:
        base_map = WorldMap(resolution="c")
        base_map.scatter_infections(state, max_infected=0.1, time=i)
        base_map.save_fig(fig_name)
        break
