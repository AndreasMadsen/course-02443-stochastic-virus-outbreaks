import _setup

from display import WorldMap
from simulator import State, Simulator
from world import regions, routes

state = State(regions, routes)
state.set_outbreak('Paris', 1000)

sim = Simulator(state)

# plot regions on a world map
base_map = WorldMap(resolution="c")
base_map.animate(sim)
base_map.show()
