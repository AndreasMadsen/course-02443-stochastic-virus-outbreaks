import _setup

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

from simulator import State, Simulator
from world import regions, routes


def plot_sir(sols, names, fig_name):
    n = len(sols)
    plt.subplots(figsize=(20,14))
    for i in range(1, n+1):
        # share x-axis
        if i == 1:
            ax = plt.subplot(n * 100 + 10 + i)
        else:
            ax = plt.subplot(n * 100 + 10 + i, sharex=ax)

        # hide x ticks except for last
        if i != n:
            plt.setp(ax.get_xticklabels(), visible=False)

        ax.set_title(names[i-1])
        sol = np.asarray(sols[i-1])

        p1, = plt.plot(sol[:, 0], color='SteelBlue', alpha=0.5, label='Susceptible')
        p2, = plt.plot(sol[:, 1], color='IndianRed', alpha=0.5, label='Infected')
        p3, = plt.plot(sol[:, 2], color='Olive', alpha=0.5, label='Removed')
        p4, = plt.plot(sol[:, 3], color='Gray', alpha=0.5, label='Total')
        plt.legend([p1, p2, p3, p4], ['S', 'I', 'R', 'T'])

    plt.savefig(fig_name, format='pdf', dpi=1000, bbox_inches='tight')


def execute_simulation(add_rio=False, rio_start=0, rio_length=18,
                       rio_visitors=380e3):
    state = State(regions, routes, verbose=True)
    state.set_outbreak('Rio De Janeiro', 1e3)#'Rio De Janeiro', 1000)
    sim = Simulator(state, transfer_prob=0.005, verbose=True)


    sol_rio = []
    sol_moscow = []
    sol_berlin = []
    sol_beijing = []
    sol_sydney = []
    sol_new_york = []
    for i, state in enumerate(sim.run(iterations=365)):
        if i == rio_start and add_rio: # start outbreak x days before olympics
            sim.add_event(2560, days=rio_length, total_transfer=rio_visitors)

        sol_rio.append(state.region_sir[2560].as_tuple(total=True))
        sol_moscow.append(state.region_sir[4029].as_tuple(total=True))
        sol_berlin.append(state.region_sir[351].as_tuple(total=True))
        sol_beijing.append(state.region_sir[3364].as_tuple(total=True))
        sol_sydney.append(state.region_sir[3361].as_tuple(total=True))
        sol_new_york.append(state.region_sir[3797].as_tuple(total=True))

    if add_rio:
        fig_name = "rio-{0}-{1}-{2}.pdf".format(rio_start, rio_length,
                                                rio_visitors)
    else:
        fig_name = "no_rio.pdf"

    plot_sir([sol_rio, sol_new_york, sol_berlin,
              sol_moscow, sol_beijing, sol_sydney],
             ['Rio De Janeiro', 'New York', 'Berlin',
              'Moscow', 'Beijing', 'Sydney'], fig_name)

if __name__ == "__main__":
    execute_simulation(True)
    execute_simulation(False)



