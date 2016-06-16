
import _setup

import scipy.stats
import math
import numpy as np

import sir
import world
from simulator import Simulator, State

state = State(world.regions, world.routes)
state.set_outbreak('Paris', 1000)

for i in range(0, 5):
    sim = Simulator(state, transfer_prob=0.005, beta=0.1, gamma=0.05)
    param_est = sir.ParameterEstimator(sim.run(iterations=700), method='regression')
    print(str(param_est))

dataAmax = np.asarray([
    # gamma, beta, N, I, max_infected, max_infected_i
    [1.560379, 7.902678, 7399998550, 1000, 4711474975, 226],
    [1.560929, 7.895128, 7399998550, 1000, 4709601783, 226],
    [1.559957, 7.901132, 7399998550, 1000, 4712761367, 226],
    [1.560943, 7.902810, 7399998550, 1000, 4709715229, 226],
    [1.559203, 7.892430, 7399998550, 1000, 4714939696, 226]
])

dataBmax = np.asarray([
    # gamma, beta, N, I, max_infected, max_infected_i
    [1.560588, 7.909428, 7399998550, 1000, 4710960293, 225],
    [1.560661, 7.904533, 7399998550, 1000, 4710630200, 226],
    [1.560394, 7.910906, 7399998550, 1000, 4711593515, 225],
    [1.560633, 7.904080, 7399998550, 1000, 4710711021, 226],
    [1.560878, 7.907631, 7399998550, 1000, 4710015591, 226]
])

dataCmax = np.asarray([
    [1.560995, 7.906910, 7399998550, 1000, 4709637924, 226],
    [1.561029, 7.909779, 7399998550, 1000, 4709589699, 226],
    [1.560426, 7.906666, 7399998550, 1000, 4711408481, 226],
    [1.562685, 7.904597, 7399998550, 1000, 4704323149, 226],
    [1.560390, 7.911855, 7399998550, 1000, 4711624896, 225]
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

def control_variate_est(data):
    N = data.shape[0]
    gamma = data[:, 0]
    infected = data[:, 4]
    print(np.corrcoef(gamma, infected))

    c = - np.cov(gamma, infected)[1, 0] / np.var(gamma, ddof=1)
    control = infected + c * (gamma - np.mean(gamma))

    infected_mean = np.mean(infected)
    infected_std = np.std(infected, ddof=1)

    control_mean = np.mean(control)
    control_std = np.std(control, ddof=3)

    ci_control = scipy.stats.t.ppf(0.975, N - 1) * control_std / math.sqrt(N)
    ci_infected = scipy.stats.t.ppf(0.975, N - 1) * infected_std / math.sqrt(N)

    print('crude mean: %f ± %f' % (infected_mean, ci_infected))
    print('control mean: %f ± %f' % (control_mean, ci_control))
    print('var(x)/var(z): %f' % (infected_std / control_std)**2)

    return (control_mean, control_std, N)

def unpaired_t_test(a_mean, a_std, a_n, b_mean, b_std, b_n):
    s = math.sqrt(a_std**2 / a_n + b_std**2 / b_n)

    df_top = (a_std**2 / a_n + b_std**2 / b_n)**2
    df_bottom = (a_std**2 / a_n)**2 / (a_n - 1) + (b_std**2 / b_n)**2 / (b_n - 1)
    df = df_top / df_bottom

    t = abs((a_mean - b_mean) / s)

    return 2 * (1 - scipy.stats.t.cdf(t, df))

print("p = %.10f" % unpaired_t_test(*control_variate_est(dataA), *control_variate_est(dataC)))
print("p = %.10f" % unpaired_t_test(*control_variate_exp(), *control_variate_exp()))
