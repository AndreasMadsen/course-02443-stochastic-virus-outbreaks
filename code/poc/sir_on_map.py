import _setup

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

from simulator import State
from world import regions, routes

if __name__ == "__main__":
    plt.figure()
    for i in range(0, 1):
        print('run {0:d}'.format(i))
        state = State(regions, routes)
        state.set_outbreak('Paris', 1000, verbose=True) # start outbreak
        sol = [state.total_SIR()]
        #sol = [state.region_sir[1382].get_sir()]
        for j in range(1, 365):
            if j % 100 == 0:
                print('step {0:d}'.format(j))

            state.step(transfer_prob=0.05)
            sol = sol + [state.total_SIR()]
            #sol = sol + [state.region_sir[1382].get_sir()]

        sol = np.asarray(sol)

        p1, = plt.plot(sol[:, 0], color='SteelBlue', alpha=0.5, label='S')
        p2, = plt.plot(sol[:, 1], color='IndianRed', alpha=0.5, label='I')
        p3, = plt.plot(sol[:, 2], color='Olive', alpha=0.5, label='R')

    print(np.sum(sol, axis=0))
    plt.legend([p1, p2, p3], ['S', 'I', 'R'])
    #plt.legend([p2, p3], ['I', 'R'])
    plt.show()
