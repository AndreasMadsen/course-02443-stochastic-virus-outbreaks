import _setup

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

from poc.sir_mc import SIR

def add_results(x, y):
    return (x[0] + y[0], x[1] + y[1], x[2] + y[2])


f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(16,10))
for i in range(0, 10):
    print('run %d' % i)
    #area 1
    sir1 = SIR(N=50)

    #area 2
    sir2 = SIR(N=50, beta=sir1.beta*3) #*10

    sol_1 = [sir1.init()]
    sol_2 = [sir2.init()]
    transfer_prob = 0.001
    for i in range(1, 30000):

        s_1_to_2 = np.random.binomial(sir1.S, transfer_prob)
        i_1_to_2 = np.random.binomial(sir1.I, transfer_prob)
        r_1_to_2 = np.random.binomial(sir1.R, transfer_prob)

        s_2_to_1 = np.random.binomial(sir2.S, transfer_prob)
        i_2_to_1 = np.random.binomial(sir2.I, transfer_prob)
        r_2_to_1 = np.random.binomial(sir2.R, transfer_prob)

        sir1.S += s_2_to_1 - s_1_to_2
        sir2.S += s_1_to_2 - s_2_to_1

        sir1.I += i_2_to_1 - i_1_to_2
        sir2.I += i_1_to_2 - i_2_to_1

        sir1.R += r_2_to_1 - r_1_to_2
        sir2.R += r_1_to_2 - r_2_to_1

        sol_1 = sol_1 + [sir1.step()]
        sol_2 = sol_2 + [sir2.step()]

    sol_1 = np.asarray(sol_1)
    sol_2 = np.asarray(sol_2)


    p1_1, = ax1.plot(sol_1[:, 0] / np.sum(sol_1, axis=1), color='SteelBlue', alpha=0.5, label='S')
    p1_2, = ax1.plot(sol_1[:, 1] / np.sum(sol_1, axis=1), color='IndianRed', alpha=0.5, label='I')
    p1_3, = ax1.plot(sol_1[:, 2] / np.sum(sol_1, axis=1), color='Olive', alpha=0.5, label='R')

    p2_1, = ax2.plot(sol_2[:, 0] / np.sum(sol_2, axis=1), color='SteelBlue', alpha=0.5, label='S')
    p2_2, = ax2.plot(sol_2[:, 1] / np.sum(sol_2, axis=1), color='IndianRed', alpha=0.5, label='I')
    p2_3, = ax2.plot(sol_2[:, 2] / np.sum(sol_2, axis=1), color='Olive', alpha=0.5, label='R')


ax1.legend([p1_1, p1_2, p1_3], ['S', 'I', 'R'])
ax1.set_title('region 1')
ax2.legend([p2_1, p2_2, p2_3], ['S', 'I', 'R'])
ax2.set_title("region 2")
plt.show(f)
