
import _setup
from nose.tools import *

from simulator.sir import SIR

def test_inc_infected():
    sir = SIR(2000, 1000, 0)
    sir.inc_infected(1000)
    assert_equal(sir, SIR(1000, 2000, 0))

def test_inc_removed():
    sir = SIR(2000, 2000, 1000)
    sir.inc_removed(1000)
    assert_equal(sir, SIR(1000, 1000, 1000))

def test_add():
    sir = SIR(1000, 2000, 3000)
    sir += SIR(10, 20, 30)
    assert_equal(sir, SIR(1010, 2020, 3030))

def test_copy():
    base_sir = SIR(1000, 2000, 3000)
    sir = base_sir.copy()
    sir.susceptible += 10
    assert_equal(base_sir, SIR(1000, 2000, 3000))
    assert_equal(sir, SIR(1010, 2000, 3000))
