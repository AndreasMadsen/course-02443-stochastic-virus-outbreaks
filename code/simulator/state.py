
import collections


from .sir import SIR


class State:
    """ State class representing a multi-compartment sir model
    """
    def __init__(self, regions, routes, beta=0.1, gamma=0.01, verbose=False):
        self._verbose = verbose
        self.regions = regions
        self.routes = routes

        self.region_sir = dict()
        for region in regions.values():
            self.region_sir[region.id] = SIR(region.population, 0, 0, region.id)

    def _print(self, *msg):
        if self._verbose: print(*msg)

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

        # Create the outbreak
        self._print("starting outbreak: city = {city}, id = {id}".format(
            city=city,
            id=outbreak_region.id
        ))
        self.region_sir[outbreak_region.id].inc_infected(infected)

    def copy(self):
        """Copy the current state
        """
        state_copy = State(self.regions, self.routes)

        for region_id, sir in self.region_sir.items():
            state_copy.region_sir[region_id].replace(sir)

        return state_copy

    def total_sir(self):
        """Used for getting the total number of susceptible, infected and removed
        accross all regions

        Parameters
        ----------
        None : uses the class object

        Returns
        -------
        SIR object
        """
        return sum(self.region_sir.values())
