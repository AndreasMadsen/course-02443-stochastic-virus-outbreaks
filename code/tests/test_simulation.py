
import _setup
from nose.tools import *

from simulator import State, Simulator
from world import regions, routes


def test_simulate():
    state = State(regions, routes)
    state.set_outbreak('Paris', 1000)

    sim = Simulator(state)

    total_population_pre = sim.state.total_sir().total_pop
    sim.step()
    total_population_post = sim.state.total_sir().total_pop

    # check that transfers and disease spread didn't change the world
    # population'
    assert_equal(total_population_pre, total_population_post)
