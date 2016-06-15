
import _setup
from nose.tools import *

from simulator import State
from world import regions, routes

def test_set_outbreak():
    state = State(regions, routes)

    assert_equal(state.region_sir[1382].susceptible, 4756)
    assert_equal(state.region_sir[1382].infected, 0)
    assert_equal(state.region_sir[1382].removed, 0)

    state.set_outbreak('Paris', 1000)

    assert_equal(state.region_sir[1382].susceptible, 3756)
    assert_equal(state.region_sir[1382].infected, 1000)
    assert_equal(state.region_sir[1382].removed, 0)

def test_copy():
    base_state = State(regions, routes)
    state = base_state.copy()
    state.set_outbreak('Paris', 1000)

    assert_equal(base_state.region_sir[1382].susceptible, 4756)
    assert_equal(base_state.region_sir[1382].infected, 0)
    assert_equal(base_state.region_sir[1382].removed, 0)

    assert_equal(state.region_sir[1382].susceptible, 3756)
    assert_equal(state.region_sir[1382].infected, 1000)
    assert_equal(state.region_sir[1382].removed, 0)

