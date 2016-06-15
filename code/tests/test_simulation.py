
import _setup
from nose.tools import *

from simulator import State
from world import regions, routes

def test_step():
    state = State(regions, routes)
    state.set_outbreak('Paris', 1000)
    total_population_pre = sum(state.total_SIR())

    state.step(verbose=True)
    total_population_post = sum(state.total_SIR())

    #check that transfers and disease spread didn't change the world population'
    assert_equal(total_population_pre, total_population_post)
