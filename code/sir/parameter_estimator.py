
import math
import textwrap

import numpy as np
from scipy.optimize import curve_fit

def _exp_func(x, A, k):
    return A * np.exp(k * x)

class ParameterEstimator:
    def __init__(self, sir_iterator, method='max'):
        if method == 'max':
            self._max_estimator(sir_iterator)
        elif method == 'regression':
            self._regression_estimator(sir_iterator)
        else:
            raise NotImplementedError('method %s is not implemented' % method)

    def _regression_estimator(self, sir_iterator):
        # Get initialization constant
        first_sir = next(sir_iterator).total_sir()
        self.population = first_sir.total_pop
        self.init_infected = first_sir.infected

        # Count infected in each time step and find the final removed
        infected = [self.init_infected]
        final_removed = 0
        for state in sir_iterator:
            total = state.total_sir()
            final_removed = total.removed
            infected.append(total.infected)

        infected = np.asarray(infected)
        time = np.arange(0, infected.size)

        # extract head
        head_infected = infected[0:250]
        head_time = time[0:250]

        # extract tail
        tail_infected = infected[440:]
        tail_time = time[440:]

        # Fint exp curve
        (A, k1), _ = curve_fit(_exp_func, head_time, head_infected)
        (B, k2), _ = curve_fit(_exp_func, tail_time, tail_infected)

        # Estimate beta and gamma
        survival_rate = (self.population - final_removed) / self.population
        self.beta = (k1 - k2) / (1 - survival_rate)
        self.gamma = (k1 * survival_rate - k2) / (1  - survival_rate)

    def _max_estimator(self, sir_iterator):
        # Get initialization constant
        first_sir = next(sir_iterator).total_sir()
        self.population = first_sir.total_pop
        self.init_infected = first_sir.infected

        # calculate final survival rate and max infected
        max_infected = 0
        max_infected_i = 0
        max_removed = 0
        final_removed = 0

        for i, state in enumerate(sir_iterator):
            total = state.total_sir()

            final_removed = total.removed

            if total.infected > max_infected:
                max_infected = total.infected
                max_infected_i = i + 1

            if total.removed > max_removed:
                max_removed = total.removed

        # calculate gamma and beta
        survival_rate = (self.population - final_removed) / self.population
        frac_beta_gamma = - math.log(survival_rate) / (1 - survival_rate)

        self.gamma = max_removed / max_infected
        self.beta = frac_beta_gamma * self.gamma

        print('max_infected = %d' % max_infected)
        print('max_infected_i = %d' % max_infected_i)

    def __str__(self):
        return "Estimator(gamma=%f, beta=%f, N=%d, I=%d)" % (
            self.gamma, self.beta, self.population, self.init_infected
        )
