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
        state = State(regions, routes)
        state.set_outbreak('Paris', 1000, verbose=True)  # start outbreak
        sim = Simulator(state, transfer_prob=0.05)

        state_list = sim.run(iterations=365, verbose=True)

        sol = [x.total_sir().as_tuple() for x in state_list]
        sol = np.asarray(sol)

        if DO_PLOT:
            p1, = plt.plot(sol[:, 0], color='SteelBlue', alpha=0.5, label='S')
            p2, = plt.plot(sol[:, 1], color='IndianRed', alpha=0.5, label='I')
            p3, = plt.plot(sol[:, 2], color='Olive', alpha=0.5, label='R')

    #print(np.sum(sol, axis=0))
    if DO_PLOT:
        plt.legend([p1, p2, p3], ['S', 'I', 'R'])
        plt.show()
