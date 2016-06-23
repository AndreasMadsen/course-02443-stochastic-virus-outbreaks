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



# param_list = []
# for i in range(0, 10):
#     print("run {0}".format(i))
#     state = State(world.regions, world.routes)
#     state.set_outbreak('Rio De Janeiro', 1e3)
#     sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5, verbose=True)
#     param_est = sir.ParameterEstimator(sim.run(iterations=120), method='max')
#     param_list.append(str(param_est))

# for x in param_list:
#     print(x)

testA = np.asarray([
    [21.378635, 44.955581, 7399998550, 1000, 284777516, 68],
    [20.734273, 43.602728, 7399998550, 1000, 293636123, 67],
    [21.202771, 44.585848, 7399998550, 1000, 287139873, 67],
    [20.985683, 44.131009, 7399998550, 1000, 290116707, 67],
    [20.568666, 43.255329, 7399998550, 1000, 296003800, 67],
    [20.752539, 43.639536, 7399998550, 1000, 293371254, 67],
    [20.731071, 43.593532, 7399998550, 1000, 293671603, 67],
    [21.153215, 44.486593, 7399998550, 1000, 287831606, 67],
    [21.116007, 44.405330, 7399998550, 1000, 288327158, 67],
    [20.863311, 43.871540, 7399998550, 1000, 291809938, 67]
])

testB = np.asarray([
    [20.694601, 43.519162, 7399998550, 1000, 294198473, 67],
    [20.855396, 43.859318, 7399998550, 1000, 291938171, 67],
    [21.004362, 44.172468, 7399998550, 1000, 289867195, 68],
    [20.915736, 43.983996, 7399998550, 1000, 291087233, 67],
    [20.899815, 43.949084, 7399998550, 1000, 291303335, 67],
    [21.202466, 44.584883, 7399998550, 1000, 287142762, 67],
    [21.019234, 44.200160, 7399998550, 1000, 289648149, 67],
    [20.925247, 44.002673, 7399998550, 1000, 290949721, 67],
    [21.328593, 44.851539, 7399998550, 1000, 285450173, 67],
    [20.700075, 43.528967, 7399998550, 1000, 294113807, 67]
])

run_with_y = [589245580.0, 590519293.0, 588610938.0, 591610513.0, 592059162.0,
             590816740.0, 589616240.0, 591010298.0, 589786057.0, 589501464.0]
run_with_x = [22.033894264113439, 21.987251012947794, 22.05910098098035,
              21.948648708624969, 21.933634416752351, 21.976369438318873,
              22.020430917626964, 21.971143010490945, 22.015058691890282,
              22.025952347097835]


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
    std_z = np.std(z, ddof=2)


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

X_0 = testA[:, 1]
Y_0 = testA[:, -2]




mean_1, std_1, n_1 = control_variate_est(run_with_y, run_with_x, verbose=True)

mean_1, std_1, n_1 = control_variate_est(Y_0, X_0, verbose=True)
mean_2, std_2, n_2 = control_variate_est(testB[:, -2], testB[:, 1], verbose=True)
print(mean_1, std_1, mean_2, std_2)


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
