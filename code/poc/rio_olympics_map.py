import _setup

from display import WorldMap
from simulator import State, Simulator
from world import regions, routes

state = State(regions, routes, verbose=True)
state.set_outbreak('Rio De Janeiro', 1000)

# sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5, verbose=True)
# sim.add_event(2560, days=18, total_transfer=380e3)
# # plot regions on a world map
# base_map = WorldMap(resolution="c")
# base_map.animate(sim, frames=120, max_infected=0.1)
# base_map.show()

sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5, verbose=True)
# plot regions on a world map
base_map = WorldMap(resolution="c")
base_map.animate(sim, frames=120, max_infected=0.1)
base_map.show()
