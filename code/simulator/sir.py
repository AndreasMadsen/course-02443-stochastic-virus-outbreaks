
class SIR:

    def __init__(self, susceptible, infected, removed):
        self.susceptible = susceptible
        self.infected = infected
        self.removed = removed
        self.total_pop = susceptible + infected + removed

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
            self.total_pop += other.total_pop
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
        self.total_pop = self.susceptible + self.infected + self.removed

    def inc_infected(self, infected):
        self.susceptible -= infected
        self.infected += infected

    def inc_removed(self, removed):
        self.infected -= removed
        self.removed += removed

    def as_tuple(self, total=False):
        if total:
            return (
                self.susceptible, self.infected,
                self.removed, self.total_pop
            )
        else:
            return (self.susceptible, self.infected, self.removed)

    def transfer_to(self, add_s, add_i, add_r):
        """ transfers people to sir object

        Parameters
        ----------
        add_s (Int) : wanted increase of susceptible
        add_i (Int) : wanted increase of infected
        add_r (Int) : wanted increase of removed

        Returns
        -------
        None : Mutates the SIR object
        """

        self.susceptible += add_s
        self.infected += add_i
        self.removed += add_r
        self.total_pop += add_s + add_i + add_r
        if self.total_pop < 0:
            raise Exception("total population < 0 after transferring to region")

    def transfer_from(self, rem_s, rem_i, rem_r):
        """ transfers people to sir object

        Parameters
        ----------
        rem_s (Int) : wanted removal of susceptible
        rem_i (Int) : wanted removal of infected
        rem_r (Int) : wanted removal of removed

        Returns
        -------
        None : Mutates the SIR object
        """

        self.susceptible -= rem_s
        self.infected -= rem_i
        self.removed -= rem_r
        self.total_pop -= rem_s + rem_i + rem_r
        if self.total_pop < 0:
            raise Exception("total population < 0 after transferring from region")
