import _setup

from display import WorldMap
from simulator import State, Simulator
from world import regions, routes

state = State(regions, routes, verbose=True)
state.set_outbreak('Sidney', 1000)

sim = Simulator(state, transfer_prob=0.005)

# plot regions on a world map
base_map = WorldMap(resolution="c")
base_map.animate(sim)
base_map.show()
