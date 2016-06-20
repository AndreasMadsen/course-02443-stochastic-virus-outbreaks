""" Defines objects used for simulating compartment sir model"""

import time
import numpy as np
import random
import textwrap
import collections

from ._time_left import TimeLeft
from ._dirichlet_sampler import sample_dirichlet

SirPair = collections.namedtuple('SirPair', ['current', 'prev'])

class Simulator:
    """CLass used for simulating compartmentalized SIR models
    """
    def __init__(self, init_state,
                 beta=0.1, gamma=0.01, transfer_prob=0.005,
                 verbose=False):
        self.state = init_state.copy()
        self.beta = beta
        self.gamma = gamma
        self.transfer_prob = transfer_prob

        self._verbose = verbose

    def _print(self, *msg):
        if (self._verbose): print(*msg)

    def run(self, iterations=365):
        """
        run n simulation iterations from the current state

        Parameters
        ---------
        iterations (Int): Number of iterations to run. Defaults to 365.

        Returns
        -------
        states (List(State)) : sets the .state_list dictionary to \
        key-value pairs (time_step, state)
        """

        yield self.state.copy()

        estimator = TimeLeft(iterations)

        # used for moving average time estimate
        for i in range(1, iterations + 1):
            (time_usage, time_left) = estimator.run(self.step)

            # if verbose print
            self._print(textwrap.dedent("""\
            Iteration {0:d}/{1:d} took {2:.2f} sec ({3:.2f} sec left)
                {4:s}
            """).format(
                i, iterations,
                time_usage, time_left,
                str(self.state.total_sir())
            ))

            yield self.state.copy()

    def update_single_region(self, region_sir):
        """Spreads the virus and updates removed within region
        """
        n_people = region_sir.total_pop

        # If there are 0 people, nothing is changed
        if n_people == 0: return

        if region_sir.infected / n_people > 1:
            print(region_sir.infected, n_people)

        # the virus spreads:
        new_infected = np.random.binomial(
            region_sir.susceptible,
            self.beta * region_sir.infected / n_people)
        region_sir.inc_infected(new_infected)

        # some people are curred:
        new_curred = np.random.binomial(
            region_sir.infected, self.gamma)
        region_sir.inc_removed(new_curred)

    def _calculate_transfer_probabilities(self, from_sir, connected_sir):
        probability = []
        n_connections = len(connected_sir)
        for to_sir in connected_sir:
            # Calculate transfer properbility
            relative_pop = to_sir.prev.total_pop / (
                to_sir.prev.total_pop + from_sir.prev.total_pop
            )
            probability.append(self.transfer_prob * relative_pop / n_connections)
        return probability

    def _transfer_sir(self, from_sir, connected_sir):
        """transfers people from from_region to to_region
        Assumes that S/I/R classes share the same travel frequency

        Parameters
        ----------
        sir_from : SIR-object which acts as transfer source
        sir_to : SIR-object which acts as transfer target

        Returns
        -------
        None : mutates from and to regions
        """
        # Nothing can be transfered stop early
        if (from_sir.current.total_pop == 0): return

        # Calculate transfer probabilities
        probability = self._calculate_transfer_probabilities(
            from_sir, connected_sir
        )

        # total number of people to transfer from a to b
        n_people = from_sir.prev.total_pop

        # get number of people that should be transfered, this guarantees
        # that sum(transfer_people) <= n_people
        transfer_people = sample_dirichlet(probability, n_people)

        # Transfer people
        for total_transfer, to_sir in zip(transfer_people, connected_sir):
            if to_sir.prev.total_pop == 0: continue
            total_transfer = min(total_transfer, to_sir.current.total_pop, to_sir.prev.total_pop)

            # This calculates
            #   p = total_transfer / n_people
            #   s_transfer = floor(region.susceptible * p)
            # but avoids floats for speed
            s_send = (from_sir.prev.susceptible * total_transfer) // n_people
            i_send = (from_sir.prev.infected * total_transfer) // n_people
            r_send = total_transfer - s_send - i_send

            # increment/decrement counters
            from_sir.current.transfer_from(s_send, i_send, r_send)
            to_sir.current.transfer_to(s_send, i_send, r_send)

            # The other way
            s_recv = (to_sir.prev.susceptible * total_transfer) // to_sir.prev.total_pop
            i_recv = (to_sir.prev.infected * total_transfer) // to_sir.prev.total_pop

            r_recv = total_transfer - s_recv - i_recv
            r_recv = (to_sir.prev.removed * total_transfer) // to_sir.prev.total_pop

            if r_recv < 0:
                raise ValueError('r_recv: %d' % r_recv)
            if r_recv > to_sir.current.removed:
                raise ValueError('%d > %d' % (r_recv, to_sir.current.removed))

            # increment/decrement counters
            to_sir.current.transfer_from(s_recv, i_recv, r_recv)
            from_sir.current.transfer_to(s_recv, i_recv, r_recv)

    def _get_neighbours_sir(self, region, prev_state):
        sir = []
        for neighbour_region in region.neighbors:
            neighbour_id = neighbour_region.id
            neighbour_sir = self.state.region_sir[neighbour_id]
            prev_neighbour_sir = prev_state.region_sir[neighbour_id]

            sir.append(SirPair(neighbour_sir, prev_neighbour_sir))
        return sir

    def _get_airlines_sir(self, region, prev_state):
        sir = []
        for route in region.airlines:
            neighbour_id = route.destination.id
            neighbour_sir = self.state.region_sir[neighbour_id]
            prev_neighbour_sir = prev_state.region_sir[neighbour_id]

            sir.append(SirPair(neighbour_sir, prev_neighbour_sir))
        return sir

    def step(self, verbose=False):
        """Advances the state to the next time point by both accounting for
        virus spreading within a reigon and transfers by commuting
        to the neighbours and by plane to connected cities
        """

        # update diseases
        for region in self.state.region_sir.values():
            self.update_single_region(region)

        # transfer people from region to neighbours and airline connected
        # regions
        prev_state = self.state.copy()
        for region_id, region in self.state.regions.items():
            region_sir = self.state.region_sir[region_id]
            prev_region_sir = prev_state.region_sir[region_id]

            # skip regions with no people as people are only transfer from
            # the region
            if (region_sir.total_pop == 0 and prev_region_sir.total_pop == 0):
                continue

            # get connected sir objects, the result is a list of pairs of
            # mutable and immutable sir objects for both neighbour and
            # airlines
            neighbors_sir = self._get_neighbours_sir(region, prev_state)
            airlines_sir = self._get_airlines_sir(region, prev_state)
            sir = neighbors_sir + airlines_sir

            # Transfer from region to neighbour
            self._transfer_sir(SirPair(region_sir, prev_region_sir), sir)
