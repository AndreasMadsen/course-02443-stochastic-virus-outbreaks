import _setup

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

from simulator import State, Simulator
from world import regions, routes

if __name__ == "__main__":
    DO_PLOT = True
    if DO_PLOT:
        plt.figure()
    for i in range(0, 1):
        print('run {0:d}'.format(i))
        state = State(regions, routes, verbose=True)
        state.set_outbreak('Paris', 1000)
        sim = Simulator(state, transfer_prob=0.005, verbose=True)

        sol = []
        for state in sim.run(iterations=10):
            #sol.append(state.total_sir().as_tuple(total=True))
            sol.append(state.region_sir[4029].as_tuple(total=True))
            print(sim.moskva)

        sol = np.asarray(sol)


        if DO_PLOT:
            p1, = plt.plot(sol[:, 0], color='SteelBlue', alpha=0.5, label='Susceptible')
            p2, = plt.plot(sol[:, 1], color='IndianRed', alpha=0.5, label='Infected')
            p3, = plt.plot(sol[:, 2], color='Olive', alpha=0.5, label='Removed')
            p4, = plt.plot(sol[:, 3], color='Gray', alpha=0.5, label='Total')

    #print(np.sum(sol, axis=0))
    if DO_PLOT:
        plt.legend([p1, p2, p3, p4], ['S', 'I', 'R', 'T'])
        plt.show()
