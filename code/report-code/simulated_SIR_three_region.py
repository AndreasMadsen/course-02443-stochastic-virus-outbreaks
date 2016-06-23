import _setup

import os.path as path

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

from world import Region, Route
from simulator import Simulator, State

thisdir = path.dirname(path.realpath(__file__))

def create_region(id, population):
    return Region({
        'airport_id': id,
        'latitude': 0,
        'longitude': 0,
        'name': 'Region %d' % id,
        'city': 'Region %d' % id,
        'country': 'Region %d' % id,
        'pop_sum': population,
        'NEIGHBORS': '-1'
    })

def create_route(airline_id, from_region, to_region):
    route = Route({
        'airline_id': airline_id,
        'source_airport_id': from_region.id,
        'destination_airport_id': to_region.id
    })

    # Cross reference
    route.source = from_region
    route.destination = to_region
    from_region.airlines.append(route)

    return route

N = 1000000
beta = 0.1
gamma = 0.01
tau = 0.0001
R0 = (2 / 50)

regions = {
    0: create_region(0, N),
    1: create_region(1, N),
    2: create_region(2, N)
}

routes = {
    (0, 1): create_route(0, regions[0], regions[1]),
    (1, 2): create_route(1, regions[1], regions[2]),
    (2, 0): create_route(2, regions[2], regions[0]),
}

plt.figure(figsize=(12, 6))

def solver(Y, t):
    return [- beta / sum(Y[:3]) * Y[1] * Y[0] + tau * (Y[6]-Y[0]),
            beta / sum(Y[:3]) * Y[1] * Y[0] - gamma * Y[1] + tau * (Y[7]-Y[1]),
            gamma * Y[1] + tau * (Y[8]-Y[2]),
            - beta / sum(Y[3:6]) * Y[4] * Y[3] + tau * (Y[0]-Y[3]),
            beta / sum(Y[3:6]) * Y[4] * Y[3] - gamma * Y[4] + tau * (Y[1]-Y[4]),
            gamma * Y[4] + tau * (Y[2] - Y[5]),
            - beta / sum(Y[6:]) * Y[7] * Y[6] + tau * (Y[3]-Y[6]),
            beta / sum(Y[6:]) * Y[7] * Y[6] - gamma * Y[7] + tau * (Y[4]-Y[7]),
            gamma * Y[7] + tau * (Y[5] - Y[8])]

start_infection_n1 = 2 / 50
t = np.arange(0, 365, 1)
asol = 100 * integrate.odeint(solver, [1 - R0, R0, 0,
                                       1, 0, 0,
                                       1, 0, 0], t)

plt.plot(t, asol[:, 1], ls='-', color='black', alpha=0.8, lw=2)
plt.plot(t, asol[:, 4], ls='-', color='black', alpha=0.8, lw=2)
ptrue, = plt.plot(t, asol[:, 7], ls='-', color='black', alpha=0.8, lw=2)

for i in range(0, 10):
    state = State(regions, routes, verbose=True)
    state.set_outbreak('Region 0', R0 * N)
    sim = Simulator(state, transfer_prob=tau, beta=beta, gamma=gamma, verbose=True)

    solution = np.zeros((365+1, 9))
    for i, state in enumerate(sim.run(iterations=365)):
        print(i)
        for region_id, sir in state.region_sir.items():
            print(str(sir))
            solution[i, region_id * 3 + 0] = state.region_sir[region_id].susceptible / N
            solution[i, region_id * 3 + 1] = state.region_sir[region_id].infected / N
            solution[i, region_id * 3 + 2] = state.region_sir[region_id].removed / N

    asol = np.asarray(solution) * 100
    t = np.arange(0, asol.shape[0])

    p1, = plt.plot(t, asol[:, 0], ls='-', color='SteelBlue')
    p2, = plt.plot(t, asol[:, 1], ls='-', color='IndianRed')
    p3, = plt.plot(t, asol[:, 2], ls='-', color='Olive')
    p4, = plt.plot(t, asol[:, 3], ls=':', color='SteelBlue')
    p5, = plt.plot(t, asol[:, 4], ls=':', color='IndianRed')
    p6, = plt.plot(t, asol[:, 5], ls=':', color='Olive')
    p7, = plt.plot(t, asol[:, 6], ls='--', color='SteelBlue')
    p8, = plt.plot(t, asol[:, 7], ls='--', color='IndianRed')
    p9, = plt.plot(t, asol[:, 8], ls='--', color='Olive')

plt.legend(
    [p1, p2, p3, p4, p5, p6, p7, p8, p9, ptrue],
    ["Susceptible 1", "Infected 1", "Recovered 1",
     "Susceptible 2", "Infected 2", "Recovered 2",
     "Susceptible 3", "Infected 3", "Recovered 3", 'Theoretical'], loc=7, fontsize=12)
plt.title("Simulated SIR 3 regions. beta={0:.2f}, gamma={1:.2f}, tau={2:.0e}, N={3:.0e}".format(
    beta, gamma, tau, N
))
plt.xlabel("Time")
plt.ylabel("% individuals")
plt.ylim(0, 100)
plt.xlim(0, 365)
plt.savefig(path.join(thisdir, '../../report/plots/sir_three_region_sim_%d.pdf' % N),
            format='pdf', dpi=1000, bbox_inches='tight')
