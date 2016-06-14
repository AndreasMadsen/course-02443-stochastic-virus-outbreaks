
import collections

from .sir import SIR

class State:
    def __init__(self, regions, routes):
        self.regions = regions
        self.routes = routes

        self.region_sir = dict()
        for region in regions.values():
            self.region_sir[region.id] = SIR(region.population, 0, 0)

    def set_outbreak(self, city, infected):
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
        self.region_sir[outbreak_region.id].inc_infected(infected)

    def copy(self):
        """Copy the current state
        """
        state_copy = State(self.regions, self.routes)

        for region_id, sir in self.region_sir.items():
            state_copy.region_sir[region_id].replace(sir)

        return state_copy
