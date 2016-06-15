""" Defines objects used for simulating compartment sir model"""

import time
import numpy as np

class Simulator:
    """CLass used for simulating compartmentalized SIR models
    """
    def __init__(self, init_state, beta=0.1, gamma=0.01, transfer_prob=0.001):
        self.state = init_state.copy()
        self.beta = beta
        self.gamma = gamma
        self.transfer_prob = transfer_prob


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

        time_step = 0
        state_list = [self.state.copy()]
        for i in range(1, iterations + 1):
            start_time = time.time()

            self.step()
            state_list = state_list + [self.state.copy()]

            end_time = time.time()
            time_diff = end_time - start_time
            time_left = time_diff * (iterations - i)
            if verbose:
                print("Iteration {0:d}/{1:d} took {2:.2f} seconds. ({3:.2f} seconds left)".format(
                    i, iterations, time_diff, time_left))

        return state_list

    def step(self, verbose=False):
        """Advances the state to the next time point by both accounting for
        virus spreading within a reigon and to the neighbours
        """

        n_transfers_processed = 0
        for region_id in self.state.region_sir.keys():
            region = self.state.regions[region_id]
            current_region_sir = self.state.region_sir[region_id]
            total_region_population = current_region_sir.total_population()
            # skip regions with no people
            if total_region_population == 0:
                continue
            # the virus spreads:
            # todo make sir_object have this parameter
            new_infected = np.random.binomial(
                current_region_sir.susceptible,
                self.beta *
                current_region_sir.infected /
                total_region_population)
            current_region_sir.inc_infected(new_infected)

            # some people are curred:
            new_curred = np.random.binomial(
                current_region_sir.infected, self.gamma)
            current_region_sir.inc_removed(new_curred)

            # for each neighbour compute a transfer of s, i and r
            for neighbour_region in region.neighbors_all:
                neighbour = self.state.region_sir[neighbour_region.id]
                # total number of people to transfer from current region to
                # current neighbour
                total_transfer = np.random.binomial(
                    total_region_population, self.transfer_prob)
                transfer_fraction = total_transfer / total_region_population

                s_transfer = np.floor(
                    current_region_sir.susceptible *
                    transfer_fraction)
                i_transfer = np.floor(
                    current_region_sir.infected *
                    transfer_fraction)
                r_transfer = np.floor(
                    current_region_sir.removed * transfer_fraction)

                current_region_sir.susceptible -= s_transfer
                neighbour.susceptible += s_transfer
                current_region_sir.infected -= i_transfer
                neighbour.infected += i_transfer
                current_region_sir.removed -= r_transfer
                neighbour.removed += r_transfer

                n_transfers_processed += 1
