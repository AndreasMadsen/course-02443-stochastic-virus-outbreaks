
import collections
import time
import numpy as np

from .sir import SIR


class State:
    """ State class representing a multi-compartment sir model
    """

    def __init__(self, regions, routes, beta=0.1, gamma=0.01):
        self.regions = regions
        self.routes = routes
        self.beta = beta
        self.gamma = gamma

        self.region_sir = dict()
        for region in regions.values():
            self.region_sir[region.id] = SIR(region.population, 0, 0)

    def set_outbreak(self, city, infected, verbose=False):
        """Create an outbreak in the busiest region in the city
        """
        # The outbreak region is the region with most airlines
        outbreak_region = None
        for region in self.regions.values():
            if region.city == city:

                if outbreak_region is None:
                    outbreak_region = region
                elif len(outbreak_region.airlines) < len(region.airlines):
                    outbreak_region = region
        if verbose:
            print(
                "starting outbreak in city '{0}' with id '{1}'".format(
                    city, outbreak_region.id))
        # Create the outbreak
        self.region_sir[outbreak_region.id].inc_infected(infected)

    def copy(self):
        """Copy the current state
        """
        state_copy = State(self.regions, self.routes)

        for region_id, sir in self.region_sir.items():
            state_copy.region_sir[region_id].replace(sir)

        return state_copy

    def total_SIR(self):
        """Used for getting the total number of susceptible, infected and removed
        accross all regions

        Parameters
        ----------
        None : uses the class object

        Returns
        -------
        3-tutple: (Susceptible, infected, removed)
        """
        total_susceptible = 0
        total_infected = 0
        total_removed = 0
        for region in self.region_sir.values():
            total_susceptible += region.susceptible
            total_infected += region.infected
            total_removed += region.removed

        return (total_susceptible, total_infected, total_removed)

    def step(self, transfer_prob=0.001, verbose=False):
        """Advances the state to the next time point by both accounting for
        virus spreading within a reigon and to the neighbours
        """
        start_time = time.time()
        n_transfers_processed = 0
        for region_id in self.region_sir.keys():
            region = self.regions[region_id]
            current_region_sir = self.region_sir[region_id]
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
                neighbour = self.region_sir[neighbour_region.id]
                # total number of people to transfer from current region to
                # current neighbour
                total_transfer = np.random.binomial(
                    total_region_population, transfer_prob)
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

        end_time = time.time()
        time_diff = end_time - start_time
        if verbose:
            print(
                """took step in {0:.2f} seconds.
             ({1:d} transfers processed ==> {2:.2f} [transfer/sec])""".format(
                    time_diff,
                    n_transfers_processed,
                    n_transfers_processed /
                    time_diff))
