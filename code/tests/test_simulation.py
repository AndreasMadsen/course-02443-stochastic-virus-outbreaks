
import _setup
from nose.tools import *

from simulator import State, Simulator
from world import regions, routes


def test_simulate():
    state = State(regions, routes)
    state.set_outbreak('Paris', 1000)
    total_population_pre = sum(state.total_SIR())

    sim = Simulator(state)
    state_list = sim.run(iterations=1, verbose=True)
    total_population_post = sum(state_list[-1].total_SIR())

    # check that transfers and disease spread didn't change the world
    # population'
    assert_equal(total_population_pre, total_population_post)
