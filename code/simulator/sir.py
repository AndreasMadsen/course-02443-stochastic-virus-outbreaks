
class SIR:
    def __init__(self, susceptible, infected, removed):
        self.susceptible = susceptible
        self.infected = infected
        self.removed = removed

    def copy(self):
        return SIR(self.susceptible, self.infected, self.removed)

    def __str__(self):
        return "SIR(S={susceptible}, I={infected}, R={removed})".format(
            susceptible=self.susceptible,
            infected=self.infected,
            removed=self.removed
        )

    # defines self == other
    def __eq__(self, other):
        return isinstance(other, SIR) and (
            self.susceptible == other.susceptible,
            self.infected == other.infected,
            self.removed == other.removed
        )

    # defines self += other
    def __iadd__(self, other):
        if isinstance(other, SIR):
            self.susceptible += other.susceptible
            self.infected += other.infected
            self.removed += other.removed
            return self
        elif other == 0:
            return self
        else:
            return NotImplemented

    # defines new = self + other
    def __add__(self, other):
        if isinstance(other, SIR):
            new = self.copy()
            return SIR.__iadd__(new, other)
        elif other == 0:
            return self.copy()
        else:
            return NotImplemented

    # defines new = other + self
    def __radd__(self, other):
        if isinstance(other, SIR):
            return SIR.__add__(self, other)
        elif other == 0:
            return self.copy()
        else:
            return NotImplemented

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
