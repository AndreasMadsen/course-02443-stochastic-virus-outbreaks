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

    def update_single_region(self, region_sir):
        """Spreads the virus and updates removed within region
        """
        n_people = region_sir.total_population()

        # the virus spreads:
        # todo make sir_object have this parameter
        new_infected = np.random.binomial(
            region_sir.susceptible,
            self.beta * region_sir.infected / n_people)

        region_sir.inc_infected(new_infected)


        # some people are curred:
        new_curred = np.random.binomial(
            region_sir.infected, self.gamma)
        region_sir.inc_removed(new_curred)

    def transfer_between_regions(self, region_sir_from, region_sir_to):
        """transfers people from from_region to to_region
        Assumes that S/I/R classes share the same travel frequency
        """

        n_people = region_sir_from.total_population()

        # total number of people to transfer from a to b
        total_transfer = np.random.binomial(n_people,
                                            self.transfer_prob)
        # convert to a probability
        transfer_fraction = total_transfer / n_people

        s_transfer = np.floor(region_sir_from.susceptible * transfer_fraction)
        i_transfer = np.floor(region_sir_from.infected * transfer_fraction)
        r_transfer = np.floor(region_sir_from.removed * transfer_fraction)

        region_sir_from.susceptible -= s_transfer
        region_sir_to.susceptible += s_transfer
        region_sir_from.infected -= i_transfer
        region_sir_to.infected += i_transfer
        region_sir_from.removed -= r_transfer
        region_sir_to.removed += r_transfer

    def step(self, verbose=False):
        """Advances the state to the next time point by both accounting for
        virus spreading within a reigon and to the neighbours
        """

        n_transfers_processed = 0
        for region_id in self.state.region_sir.keys():
            region = self.state.regions[region_id]
            current_region_sir = self.state.region_sir[region_id]

            # skip regions with no people
            if current_region_sir.total_population() == 0:
                continue

            self.update_single_region(current_region_sir)


            # for each neighbour compute a transfer of s, i and r
            for neighbour_region in region.neighbors_all:
                neighbour_sir = self.state.region_sir[neighbour_region.id]

                self.transfer_between_regions(current_region_sir,
                                              neighbour_sir)

                n_transfers_processed += 1
