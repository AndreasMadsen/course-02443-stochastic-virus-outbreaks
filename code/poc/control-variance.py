# warning nothing works as expected
# temp commit

import _setup

import scipy.stats
import math
import numpy as np
from sklearn.covariance import ShrunkCovariance
from sklearn.covariance import LedoitWolf
from sklearn.covariance import OAS

import sir
import world
from simulator import Simulator, State
"""
param_list = []
for i in range(0, 10):
    print("run {0}".format(i))
    state = State(world.regions, world.routes)
    state.set_outbreak('Rio De Janeiro', 1e3)
    sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5, verbose=True)
    param_est = sir.ParameterEstimator(
        (state.total_sir() for state in sim.run(iterations=120)),
        method='max')
    param_list.append(str(param_est))

for x in param_list:
    print(x)
"""
testA = np.asarray([
    [1.000086, 2.103098, 7399998550, 1000, 291969298, 67],
    [1.000049, 2.102964, 7399998550, 1000, 290766216, 67],
    [1.000064, 2.102972, 7399998550, 1000, 289766956, 67],
    [1.000021, 2.102957, 7399998550, 1000, 289169345, 67],
    [0.999979, 2.102798, 7399998550, 1000, 291750589, 67],
    [0.999992, 2.102972, 7399998550, 1000, 287409342, 67],
    [1.000124, 2.103241, 7399998550, 1000, 293816202, 67],
    [0.999915, 2.102727, 7399998550, 1000, 294525678, 67],
    [0.999929, 2.102690, 7399998550, 1000, 293652342, 67],
    [0.999960, 2.102823, 7399998550, 1000, 290475555, 67]
])

def control_variate_exp(N=100):
    u = np.random.uniform(size=N)
    x = np.exp(u)
    mean_x, sigma_x = np.mean(x), np.std(x, ddof=1)
    z = x + (-0.14086/(1/12)) * (u - 0.5)
    mean_z, sigma_z = np.mean(z), np.std(z, ddof=1)
    ci_x = scipy.stats.t.ppf(0.975, N - 1) * mean_x / math.sqrt(N)
    ci_z = scipy.stats.t.ppf(0.975, N - 1) * mean_z / math.sqrt(N)
    print('crude mean: %f ± %f' % (mean_x, ci_x))
    print('control mean: %f ± %f' % (mean_z, ci_z))
    print('var(x)/var(z): %f' % (sigma_x / sigma_z)**2)
    return (mean_z, sigma_z, N)

def control_variate_est(y, x, verbose=False):
    N = len(y)

    if verbose:
        print("corr:",np.corrcoef(x, y))

    c = -np.cov(x, y)[1, 0] / np.var(x, ddof=1)
    z = y + c * (x - np.mean(x))

    mu_y = np.mean(y)
    mu_z = np.mean(z)
    std_y = np.std(y, ddof=1)
    std_z = np.std(z, ddof=1)


    conf_y = scipy.stats.t.ppf(0.975, N - 1) * std_y / math.sqrt(N)
    conf_z = scipy.stats.t.ppf(0.975, N - 1) * std_z / math.sqrt(N)

    if verbose:
        print("stats:")
        print('\tcrude mean: %f ± %f' % (mu_y, conf_y))
        print('\tcontrol mean: %f ± %f' % (mu_z, conf_z))
        print('\tvar(y)/var(z): %f' % (std_y / std_z)**2)

    return (mu_z, std_z, N)

def unpaired_t_test(a_mean, a_std, a_n, b_mean, b_std, b_n):
    #print("input: ", a_mean, a_std, a_n, b_mean, b_std, b_n)
    #s = math.sqrt((a_std**2 + b_std**2) / (a_n + b_n - 2 ))
    #t = (a_mean - b_mean) / math.sqrt(s**2 * (1 / a_n + 1 / b_n))
    #df = a_n + b_n - 4

    s = math.sqrt(a_std**2 / a_n + b_std**2 / b_n)
    df_top = (a_std**2 / a_n + b_std**2 / b_n)**2
    df_bottom = (a_std**2 / a_n)**2 / (a_n - 1) + (b_std**2 / b_n)**2 / (b_n - 1)
    df = df_top / df_bottom

    t = abs((a_mean - b_mean) / s)
    #print(t, df)
    return 2 * (1 - scipy.stats.t.cdf(t, df))

mean_1, std_1, n_1 = control_variate_est(testA[:, -2], testA[:, 1], verbose=True)

"""
print("control p = {0:.10f}".format(unpaired_t_test(mean_1, std_1, n_1,
                                         mean_2, std_2, n_2)))
print("crude p = {0:.10f}".format(
    unpaired_t_test(np.mean(testA[:, -2]),
                    np.sqrt(np.var(testA[:, -2])),
                    testA.shape[0],
                    np.mean(testB[:, -2]),
                    np.sqrt(np.var(testB[:, -2])),
                    testB.shape[0])))

print(np.mean(testA[:, -2]) * 1e-6,
      np.mean(testB[:, -2]) * 1e-6)
print(np.sqrt(np.var(testA[:, -2])) * 1e-6,
      np.sqrt(np.var(testB[:, -2])) * 1e-6 )
#print("p = %.10f".format(unpaired_t_test(*control_variate_exp(), *control_variate_exp())))
"""
