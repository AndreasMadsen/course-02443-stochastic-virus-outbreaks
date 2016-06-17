""" Plots the theoretical SIR curve """

import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

N_1 = 50
N_2 = 50
N_3 = 50
beta = 0.1
gamma = 0.01

# Y=(S_1, I_1, R_1, S_2, I_2, R_2, S_3, I_3, R_3)
transfer_prob = 0.0001
def solver(Y, t):
    return [- beta / sum(Y[:3]) * Y[1] * Y[0] + transfer_prob * (Y[6]-Y[0]),
            beta / sum(Y[:3]) * Y[1] * Y[0] - gamma * Y[1] + transfer_prob * (Y[7]-Y[1]),
            gamma * Y[1] + transfer_prob * (Y[8]-Y[2]),
            - beta / sum(Y[3:6]) * Y[4] * Y[3] + transfer_prob * (Y[0]-Y[3]),
            beta / sum(Y[3:6]) * Y[4] * Y[3] - gamma * Y[4] + transfer_prob * (Y[1]-Y[4]),
            gamma * Y[4] + transfer_prob * (Y[2] - Y[5]),
            - beta / sum(Y[6:]) * Y[7] * Y[6] + transfer_prob * (Y[3]-Y[6]),
            beta / sum(Y[6:]) * Y[7] * Y[6] - gamma * Y[7] + transfer_prob * (Y[4]-Y[7]),
            gamma * Y[7] + transfer_prob * (Y[5] - Y[8])]

start_infection_n1 = 2
t = np.arange(0, 365, 0.01)
asol = integrate.odeint(solver, [N_1 - start_infection_n1,
                                 start_infection_n1,
                                 0,
                                 N_2,
                                 0,
                                 0,
                                 N_3,
                                 0,
                                 0], t)
plt.figure(figsize=(12, 8))
plt.plot(t, asol)
plt.legend(["S_1", "I_1", "R_1",
            "S_2", "I_2", "R_2",
            "S_3", "I_3", "R_3"], loc=7)
plt.title("Theorical SIR 3 regions. N_k={0:d}, Beta={1:.2f}, Gamma={2:.2f}, tau =1e-4".format(
    N_2, beta, gamma
))
plt.xlabel("Time")
plt.ylabel("# of individuals")
plt.show()
#plt.savefig('sir_three_region.pdf', format='pdf',
#            dpi=1000, bbox_inches='tight')
