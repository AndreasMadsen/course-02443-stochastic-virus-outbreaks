""" Defines objects used for simulating compartment sir model"""

import time
import numpy as np
import random
import textwrap
import collections

from ._time_left import TimeLeft
from ._dirichlet_sampler import sample_dirichlet

SirPair = collections.namedtuple('SirPair', ['current', 'prev', 'region'])

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

        self.time_to_reverse = None
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

    def add_event(self, id, days=18, total_transfer=380e3):
        """ Adds an event where people accross the globe are
        transferred to a region for a specific time period

        Parameters
        ----------
        id (int): Id of region hosting event
        days (int): Number of days that the event should last
        transfer_amount (int): Number of people to transfer to region

        Returns
        -------
        None : Mutates the Simulator object
        """
        target_region = self.state.region_sir[id]
        self.reverse_from_id = id
        self.reverse_transfer_amount = {}
        N = sum(self.state.total_sir().as_tuple())
        for key in self.state.region_sir:
            if key == id:
                continue #skip target region
            from_region = self.state.region_sir[key]
            total_from = from_region.total_pop
            if total_from == 0:
                continue #skip, there is nothign to distribute
            transfer_amount = np.round(total_transfer * total_from / N)
            self.reverse_transfer_amount[key] = transfer_amount

            send_susceptible = (transfer_amount * from_region.susceptible) // total_from
            send_infected = (transfer_amount * from_region.infected) // total_from
            send_removed = (transfer_amount * from_region.removed) // total_from

            from_region.transfer_from(send_susceptible, send_infected,
                                      send_removed)

            target_region.transfer_to(send_susceptible, send_infected,
                                      send_removed)

        self.time_to_reverse = days

    def reverse_event(self):
        from_region = self.state.region_sir[self.reverse_from_id]
        for key, transfer_amount in self.reverse_transfer_amount.items():
            to_region = self.state.region_sir[key]

            total_from = from_region.total_pop
            if total_from == 0:
                break # nothing left to distribute
            send_susceptible = (transfer_amount * from_region.susceptible) // total_from
            send_infected = (transfer_amount * from_region.infected) // total_from
            send_removed = (transfer_amount * from_region.removed) // total_from

            from_region.transfer_from(send_susceptible, send_infected,
                                      send_removed)

            to_region.transfer_to(send_susceptible, send_infected,
                                  send_removed)

    def update_single_region(self, region_sir):
        """Spreads the virus and updates removed within region
        """
        n_people = region_sir.total_pop

        # If there are 0 people, nothing is changed
        if n_people == 0: return

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
            to_connections = len(to_sir.region.airlines) + len(to_sir.region.neighbors)
            neighbors_factor = (to_connections + n_connections) / (to_connections * n_connections)
            probability.append(self.transfer_prob * neighbors_factor * relative_pop)
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
        if from_sir.current.total_pop == 0: return

        # Calculate transfer probabilities
        probability = self._calculate_transfer_probabilities(
            from_sir, connected_sir
        )

        # total number of people to transfer from a to b
        from_people = from_sir.prev.total_pop

        # get number of people that should be transfered, this guarantees
        # that sum(transfer_people) <= n_people
        transfer_people = sample_dirichlet(probability, from_people)

        # Transfer people
        for sample_transfer, to_sir in zip(transfer_people, connected_sir):
            if sample_transfer == 0: continue

            # This calculates
            #   p = total_transfer / n_people
            #   s_transfer = floor(region.susceptible * p)
            # but avoids floats for speed
            s_send = (from_sir.prev.susceptible * sample_transfer) // from_people
            i_send = (from_sir.prev.infected * sample_transfer) // from_people
            r_send = (from_sir.prev.removed * sample_transfer) // from_people

            # increment/decrement counters
            from_sir.current.transfer_from(s_send, i_send, r_send)
            to_sir.current.transfer_to(s_send, i_send, r_send)

    def _get_neighbours_sir(self, region, prev_state):
        sir = []
        for neighbour_region in region.neighbors:
            neighbour_id = neighbour_region.id
            neighbour_sir = self.state.region_sir[neighbour_id]
            prev_neighbour_sir = prev_state.region_sir[neighbour_id]

            sir.append(SirPair(neighbour_sir, prev_neighbour_sir, self.state.regions[neighbour_id]))
        return sir

    def _get_airlines_sir(self, region, prev_state):
        sir = []
        for route in region.airlines:
            neighbour_id = route.destination.id
            neighbour_sir = self.state.region_sir[neighbour_id]
            prev_neighbour_sir = prev_state.region_sir[neighbour_id]

            sir.append(SirPair(neighbour_sir, prev_neighbour_sir, self.state.regions[neighbour_id]))
        return sir

    def step(self, verbose=False):
        """Advances the state to the next time point by both accounting for
        virus spreading within a reigon and transfers by commuting
        to the neighbours and by plane to connected cities
        """

        if self.time_to_reverse is not None:
            if self.time_to_reverse > 0:
                self.time_to_reverse -= 1
            else:
                self.reverse_event()
                self.time_to_reverse = None

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
            self._transfer_sir(SirPair(region_sir, prev_region_sir, region), sir)
