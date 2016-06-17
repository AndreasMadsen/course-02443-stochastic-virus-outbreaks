""" Defines objects used for simulating compartment sir model"""

import time
import numpy as np
import random
import textwrap

from ._time_left import TimeLeft

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

        # the virus spreads:
        new_infected = np.random.binomial(
            region_sir.susceptible,
            self.beta * region_sir.infected / n_people)
        region_sir.inc_infected(new_infected)

        # some people are curred:
        new_curred = np.random.binomial(
            region_sir.infected, self.gamma)
        region_sir.inc_removed(new_curred)

    def _transfer_sir(self,
                      sir_from, sir_to,
                      prev_sir_from, prev_sir_to):
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
        if (sir_from.total_pop == 0): return

        # Calculate transfer properbility
        relative_pop = prev_sir_to.total_pop / (
            prev_sir_to.total_pop + prev_sir_from.total_pop
        )
        properbility = self.transfer_prob * relative_pop

        # total number of people to transfer from a to b
        n_people = prev_sir_from.total_pop
        total_transfer = np.random.binomial(n_people, properbility)

        # This calculates
        #   p = total_transfer / n_people
        #   s_transfer = floor(region.susceptible * p)
        # but avoids floats for speed
        s_transfer = (prev_sir_from.susceptible * total_transfer) // n_people
        i_transfer = (prev_sir_from.infected * total_transfer) // n_people
        r_transfer = total_transfer - s_transfer - i_transfer

        # check that we are not transferring more people than available
        if (s_transfer > sir_from.susceptible or
           i_transfer > sir_from.infected or
           r_transfer > sir_from.removed):
            s_transfer = min(s_transfer, sir_from.susceptible)
            i_transfer = min(i_transfer, sir_from.infected)
            r_transfer = min(r_transfer, sir_from.removed)

        # increment/decrement counters
        sir_from.transfer_from(s_transfer, i_transfer, r_transfer)
        sir_to.transfer_to(s_transfer, i_transfer, r_transfer)

    # @profile
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
            if (region_sir.total_pop == 0 and
               prev_region_sir.total_pop == 0):
                continue

            # for each neighbour compute a transfer of s, i and r
            shuffled_neighbours = random.sample(
                region.neighbors, len(region.neighbors)
            )
            for neighbour_region in shuffled_neighbours:
                # Find sir objects
                neighbour_id = neighbour_region.id
                neighbour_sir = self.state.region_sir[neighbour_id]
                prev_neighbour_sir = prev_state.region_sir[neighbour_id]

                # Transfer from region to neighbour
                self._transfer_sir(
                    region_sir, neighbour_sir,
                    prev_region_sir, prev_neighbour_sir
                )

            # for each airline route compute transfer of s, i and r
            # remember region.airlines is a list of Route
            shuffled_airlines = random.sample(
                region.airlines, len(region.airlines)
            )
            for route in shuffled_airlines:
                # Find sir objects
                neighbour_id = route.destination.id
                neighbour_sir = self.state.region_sir[neighbour_id]
                prev_neighbour_sir = prev_state.region_sir[neighbour_id]

                # Transfer from region to neighbour
                self._transfer_sir(
                    region_sir, neighbour_sir,
                    prev_region_sir, prev_neighbour_sir
                )
