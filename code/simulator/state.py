
import collections


from .sir import SIR


class State:
    """ State class representing a multi-compartment sir model
    """

    def __init__(self, regions, routes, beta=0.1, gamma=0.01):
        self.regions = regions
        self.routes = routes


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