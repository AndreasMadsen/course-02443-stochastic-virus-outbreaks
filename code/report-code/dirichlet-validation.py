
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import scipy.stats
import numpy as np
import os.path as path

thisdir = path.dirname(path.realpath(__file__))

def _calc_alpha(p_list, n):
    n_neighbors = len(p_list)

    # the last alpha is responsible for all the people that shouldn't be moved
    # its value should be (n - 1) - sum(alpha). It is accumulated
    # sequentially here.
    remain = n - 1

    # Calculate alpha and calculate the remainder sequentially
    for p in p_list:
        # If the properbility is 0 just consider the region as if it never
        # exisited
        if p > 0:
            alpha = p * (n - 1)
            yield alpha
        else:
            alpha = 0
        remain -= alpha

    # The remainder is now calculated
    yield remain

p = [0.1, 0.1]
n = 100
alpha = np.fromiter(_calc_alpha(p, n), dtype='float')

print(alpha[0], np.sum(alpha) - alpha[0])
beta = scipy.stats.beta(alpha[0], np.sum(alpha) - alpha[0])
dirichlet = scipy.stats.dirichlet(alpha)
binomial = scipy.stats.binom(n, p[0])
n = np.arange(0, 101)

# Plot marginal dirichlet distribution with binomial distribution
plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.bar(n, binomial.pmf(n), width=0.3, color='SteelBlue', lw=0, label='binomial')
plt.bar(n + 0.3,
        beta.cdf(np.minimum(1, (n + 0.5) / 101)) - beta.cdf(np.maximum(0, (n - 0.5) / 101)),
        width=0.3, color='IndianRed', lw=0, label='dirichlet')
plt.legend(fontsize=12)
plt.ylabel('properbility')
plt.xlabel('transfers')
plt.xlim(0, 100)

ax = plt.subplot(2, 1, 2, projection='3d')

X, Y = np.meshgrid(np.arange(1, 101), np.arange(1, 101))
coords = np.vstack((
    X.ravel(), Y.ravel(), 101 - X.ravel() - Y.ravel()
)).T / 101
coords = coords[coords[:, 2] > 0]

Z = dirichlet.pdf(coords.T)
ax.plot_trisurf(coords[:, 0] * 101, coords[:, 1] * 101, Z, lw=0)
ax.set_xlabel('transfers (region 1)')
ax.set_ylabel('transfers (region 2)')
ax.set_zlabel('pdf')

plt.savefig(path.join(thisdir, '../../report/plots/dirichlet-validation.pdf'),
            format='pdf', dpi=1000, bbox_inches='tight')
