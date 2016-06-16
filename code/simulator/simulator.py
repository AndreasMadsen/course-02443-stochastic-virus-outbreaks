""" Defines objects used for simulating compartment sir model"""

import time
import numpy as np
import math

class Simulator:
    """CLass used for simulating compartmentalized SIR models
    """
    def __init__(self, init_state, beta=0.1, gamma=0.01, transfer_prob=0.001):
        self.state = init_state.copy()
        self.beta = beta
        self.gamma = gamma
        self.transfer_prob = transfer_prob

    # @profile
    def run(self, iterations=365, verbose=False):
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

        # used for moving average time estimate
        iteration_time_estimate = 0
        yield self.state.copy()
        for i in range(1, iterations + 1):
            # start timing
            start_time = time.time()

            self.step()
            #state_list = state_list + [self.state.copy()]

            # end timing
            end_time = time.time()
            time_diff = end_time - start_time

            # update time estimate
            if iteration_time_estimate == 0:
                iteration_time_estimate = time_diff
            else:
                iteration_time_estimate = 0.9 * iteration_time_estimate + 0.1 * time_diff
            time_left = iteration_time_estimate * (iterations - i)

            # if verbose print
            if verbose:
                print("Iteration {0:d}/{1:d} took {2:.2f} seconds ({3:.2f} seconds left). \
                Infected={4:d} ".format(
                    i, iterations, time_diff, time_left, self.state.total_SIR()[1]))

            yield self.state.copy()


    # @profile
    def update_single_region(self, region_sir):
        """Spreads the virus and updates removed within region
        """
        n_people = region_sir.total_pop

        # the virus spreads:
        new_infected = np.random.binomial(
            region_sir.susceptible,
            self.beta * region_sir.infected / n_people)
        #region_sir.inc_infected(new_infected)
        region_sir.infected += new_infected
        region_sir.susceptible -= new_infected


        # some people are curred:
        new_curred = np.random.binomial(
            region_sir.infected, self.gamma)
        #region_sir.inc_removed(new_curred)
        region_sir.removed += new_curred
        region_sir.infected -= new_curred

    # @profile
    @classmethod
    def transfer_between_regions(cls, region_sir_from, region_sir_to, transfer_prob):
        """transfers people from from_region to to_region
        Assumes that S/I/R classes share the same travel frequency
        """

        n_people = region_sir_from.total_pop

        # total number of people to transfer from a to b

        total_transfer = np.random.binomial(n_people, transfer_prob)
        # let p = total_transfer / n_people
        # s_transfer = floor(region.susceptible * p)
        # to speed up with do the above with:
        # (region_susceptible * total_transfer) div n_people
        s_transfer = (region_sir_from.susceptible * total_transfer) // n_people
        i_transfer = (region_sir_from.infected * total_transfer) // n_people
        r_transfer = total_transfer - s_transfer - i_transfer

        region_sir_from.transfer_from(s_transfer, i_transfer, r_transfer)
        region_sir_to.transfer_to(s_transfer, i_transfer, r_transfer)

    # @profile
    def step(self, verbose=False):
        """Advances the state to the next time point by both accounting for
        virus spreading within a reigon and to the neighbours
        """

        for region_id, region in self.state.regions.items():
            current_region_sir = self.state.region_sir[region_id]

            # skip regions with no people
            if current_region_sir.total_pop == 0:
                continue

            self.update_single_region(current_region_sir)


            # for each neighbour compute a transfer of s, i and r
            n_neighbours = len(region.neighbors)
            for neighbour_region in region.neighbors:

                # check that we still have people left in the region
                if current_region_sir.total_pop == 0:
                    # no people left break
                    break

                neighbour_sir = self.state.region_sir[neighbour_region.id]

                Simulator.transfer_between_regions(
                    current_region_sir, neighbour_sir,
                    neighbour_sir.total_pop /
                    (neighbour_sir.total_pop + current_region_sir.total_pop)
                    * self.transfer_prob / n_neighbours)

            # for each airline route compute transfer of s, i and raise
            # remember region.airlines is a list of Route
            n_routes = len(region.airlines)
            for route in region.airlines:

                # check that we still have people left in the region
                if current_region_sir.total_pop == 0:
                    # no people left to distribute break
                    break

                neighbour_sir = self.state.region_sir[route.destination.id]

                Simulator.transfer_between_regions(
                    current_region_sir, neighbour_sir,
                    neighbour_sir.total_pop /
                    (neighbour_sir.total_pop + current_region_sir.total_pop)
                    * self.transfer_prob / n_routes)
