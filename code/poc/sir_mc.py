
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt


class SIR:

    def __init__(self, beta=0.1e-2, gamma=0.5e-3, B=1.5, N=30000):
        self.beta = beta
        self.gamma = gamma
        self.B = B
        self.N = N

        (self.S, self.I, self.R) = tuple(self.init())

    def init(self):
        S = self.N - self.B
        I = self.B
        R = 0
        return [S, I, R]

    def step(self):
        sick = scipy.stats.binom.rvs(self.S, self.beta * (self.I / self.N))
        removed = scipy.stats.binom.rvs(self.I, self.gamma)

        S = self.S - sick
        I = self.I + sick - removed
        R = self.R + removed

        (self.S, self.I, self.R) = (S, I, R)
        return [S, I, R]
if __name__ == "__main__":
    plt.figure()
    for i in range(0, 10):
        print('run %d' % i)
        sir = SIR(N=100)
        sol = [sir.init()] + [sir.step() for i in range(1, 30000)]
        sol = np.asarray(sol)

        p1, = plt.plot(sol[:, 0], color='SteelBlue', alpha=0.5, label='S')
        p2, = plt.plot(sol[:, 1], color='IndianRed', alpha=0.5, label='I')
        p3, = plt.plot(sol[:, 2], color='Olive', alpha=0.5, label='R')

    plt.legend([p1, p2, p3], ['S', 'I', 'R'])
    plt.show()
