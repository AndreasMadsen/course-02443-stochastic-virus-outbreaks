
import collections

class RegionSIR:
    def __init__(self, susceptible, infected, removed):
        self.susceptible = susceptible
        self.infected = infected
        self.removed = removed

    def __str__(self):
        return "RegionSIR(S={susceptible}, I={infected}, R={removed})".format(
            susceptible=self.susceptible,
            infected=self.infected,
            removed=self.removed
        )

    def replace(self, sir):
        self.susceptible = sir.susceptible
        self.infected = sir.infected
        self.removed = sir.removed

    def inc_infected(self, infected):
        self.susceptible -= infected
        self.infected += infected

    def inc_removed(self, removed):
        self.infected -= removed
        self.removed += removed

class State:
    def __init__(self, regions, routes):
        self.regions = regions
        self.routes = routes

        self.region_sir = dict()
        for region in regions.values():
            self.region_sir[region.id] = RegionSIR(region.population, 0, 0)

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
