
import _setup

import scipy.stats
import math
import numpy as np

import sir
import world
from simulator import Simulator, State
import matplotlib.pyplot as plt

state = State(world.regions, world.routes)
state.set_outbreak('Paris', 1000)

# param_list = []
# for i in range(0, 25):
#     print("run {0}".format(i))
#     sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5, verbose=True)
#     param_est = sir.ParameterEstimator(sim.run(iterations=120), method='max')
#     param_list.append(str(param_est))

# for x in param_list:
#     print(x)




sample_a = np.asarray([
     # gamma,       beta,          N,    I, max_infected, max_infected_i
    [16.921686, 35.575031, 7399998550, 1000, 359733948, 53],
    [16.725976, 35.164427, 7399998550, 1000, 363948376, 53],
    [16.994056, 35.727980, 7399998550, 1000, 358206776, 53],
    [16.858108, 35.434701, 7399998550, 1000, 361050212, 53],
    [16.680545, 35.065132, 7399998550, 1000, 364916209, 53],
    [17.077037, 35.902604, 7399998550, 1000, 356467155, 53],
    [16.710518, 35.130985, 7399998550, 1000, 364279204, 53],
    [16.805069, 35.329704, 7399998550, 1000, 362229321, 53],
    [16.591356, 34.876080, 7399998550, 1000, 366868074, 53],
    [16.693592, 35.095984, 7399998550, 1000, 364652189, 53],
    [16.661797, 35.030350, 7399998550, 1000, 365355525, 53],
    [17.079622, 35.905867, 7399998550, 1000, 356400394, 53],
    [17.043691, 35.830201, 7399998550, 1000, 357150964, 53],
    [16.722502, 35.150612, 7399998550, 1000, 363983881, 53],
    [17.039259, 35.821310, 7399998550, 1000, 357246395, 53],
    [17.037582, 35.817133, 7399998550, 1000, 357277709, 53],
    [16.589344, 34.875439, 7399998550, 1000, 366935026, 53],
    [16.998631, 35.732267, 7399998550, 1000, 358078593, 53],
    [16.599303, 34.895705, 7399998550, 1000, 366710697, 53],
    [17.046623, 35.838724, 7399998550, 1000, 357103525, 53],
    [16.970235, 35.677558, 7399998550, 1000, 358707554, 53],
    [16.807699, 35.334404, 7399998550, 1000, 362167575, 53],
    [16.804597, 35.331459, 7399998550, 1000, 362256238, 53],
    [16.635865, 34.976885, 7399998550, 1000, 365931613, 53],
    [16.882410, 35.488658, 7399998550, 1000, 360547869, 53]
])

sample_b = np.asarray([
    # gamma,       beta,          N,    I, max_infected, max_infected_i
    [17.266679, 36.300383, 7399998550, 1000, 352546725, 53],
    [16.593989, 34.885802, 7399998550, 1000, 366836065, 53],
    [16.803223, 35.326200, 7399998550, 1000, 362271408, 53],
    [16.667166, 35.037074, 7399998550, 1000, 365209561, 53],
    [16.541180, 34.776171, 7399998550, 1000, 368015972, 53],
    [17.074520, 35.898388, 7399998550, 1000, 356526055, 53],
    [16.778754, 35.272870, 7399998550, 1000, 362788154, 53],
    [16.796787, 35.307117, 7399998550, 1000, 362376308, 53],
    [16.822506, 35.367743, 7399998550, 1000, 361862239, 53],
    [16.870268, 35.467043, 7399998550, 1000, 360831037, 53],
    [16.772882, 35.262420, 7399998550, 1000, 362926784, 53],
    [16.655302, 35.018078, 7399998550, 1000, 365506604, 53],
    [16.752584, 35.217780, 7399998550, 1000, 363354422, 53],
    [16.765483, 35.244783, 7399998550, 1000, 363074184, 53],
    [16.841945, 35.406830, 7399998550, 1000, 361433777, 53],
    [17.024696, 35.793397, 7399998550, 1000, 357568040, 53],
    [16.854274, 35.432614, 7399998550, 1000, 361168558, 53],
    [16.729677, 35.171484, 7399998550, 1000, 363863408, 53],
    [17.109756, 35.963821, 7399998550, 1000, 355740923, 53],
    [16.831264, 35.385016, 7399998550, 1000, 361667016, 53],
    [16.730808, 35.172773, 7399998550, 1000, 363832109, 53],
    [16.631379, 34.965413, 7399998550, 1000, 366017599, 53],
    [16.413649, 34.509235, 7399998550, 1000, 370882943, 52],
    [16.670738, 35.047018, 7399998550, 1000, 365146392, 53],
    [16.699254, 35.106110, 7399998550, 1000, 364517566, 53]
])

##### draw 2016-06-21 12:38:
draw_1 = np.asarray([
    [16.827334, 35.374895, 7399998550, 1000, 361740198, 53],
    [16.686586, 35.080700, 7399998550, 1000, 364801832, 53],
    [16.926623, 35.588037, 7399998550, 1000, 359644816, 53],
    [16.946715, 35.627378, 7399998550, 1000, 359201020, 53],
    [16.696344, 35.101625, 7399998550, 1000, 364591184, 53],
    [16.611581, 34.923272, 7399998550, 1000, 366450611, 53],
    [16.676088, 35.059824, 7399998550, 1000, 365038898, 53],
    [16.984031, 35.708962, 7399998550, 1000, 358430512, 52],
    [16.716247, 35.142568, 7399998550, 1000, 364151538, 53],
    [16.584603, 34.865866, 7399998550, 1000, 367042383, 52],
    [16.797382, 35.315354, 7399998550, 1000, 362406113, 53],
    [17.231728, 36.226368, 7399998550, 1000, 353258652, 53],
    [16.795062, 35.306066, 7399998550, 1000, 362429273, 53],
    [16.962192, 35.659890, 7399998550, 1000, 358873110, 53],
    [16.674659, 35.050744, 7399998550, 1000, 365032546, 53],
    [17.025064, 35.794235, 7399998550, 1000, 357560703, 53],
    [16.599260, 34.895665, 7399998550, 1000, 366711944, 53],
    [16.846799, 35.416773, 7399998550, 1000, 361328059, 53],
    [17.017508, 35.777156, 7399998550, 1000, 357712372, 53],
    [17.083380, 35.915952, 7399998550, 1000, 356334868, 53],
    [16.718850, 35.146077, 7399998550, 1000, 364082755, 53],
    [16.752219, 35.216887, 7399998550, 1000, 363361567, 53],
    [16.741820, 35.196696, 7399998550, 1000, 363597543, 53],
    [16.809864, 35.341097, 7399998550, 1000, 362133973, 53],
    [16.771507, 35.258166, 7399998550, 1000, 362948182, 53]
])

#### draw 2016-06-21 13:15:
draw_2 = np.asarray([
    [16.577305, 34.851722, 7399998550, 1000, 367211494, 53],
    [16.908159, 35.543038, 7399998550, 1000, 360000327, 52],
    [16.467373, 34.620122, 7399998550, 1000, 369659854, 53],
    [16.895760, 35.519731, 7399998550, 1000, 360281148, 53],
    [16.885041, 35.494120, 7399998550, 1000, 360491270, 53],
    [16.682347, 35.066791, 7399998550, 1000, 364863603, 53],
    [16.519312, 34.728734, 7399998550, 1000, 368493910, 53],
    [16.762503, 35.239095, 7399998550, 1000, 363142269, 53],
    [16.838340, 35.400983, 7399998550, 1000, 361521673, 53],
    [17.350424, 36.475556, 7399998550, 1000, 350839992, 53],
    [16.930217, 35.593224, 7399998550, 1000, 359554228, 53],
    [16.985040, 35.707104, 7399998550, 1000, 358385471, 53],
    [16.794143, 35.305766, 7399998550, 1000, 362459053, 53],
    [16.700036, 35.108666, 7399998550, 1000, 364506121, 53],
    [16.802920, 35.326545, 7399998550, 1000, 362283930, 53],
    [16.730823, 35.170140, 7399998550, 1000, 363815376, 53],
    [16.789862, 35.297364, 7399998550, 1000, 362555120, 53],
    [16.923378, 35.579225, 7399998550, 1000, 359701789, 53],
    [16.841513, 35.407157, 7399998550, 1000, 361450547, 53],
    [16.644576, 34.994141, 7399998550, 1000, 365733505, 53],
    [16.843054, 35.409145, 7399998550, 1000, 361409878, 53],
    [16.898729, 35.524852, 7399998550, 1000, 360211081, 53],
    [16.767846, 35.252385, 7399998550, 1000, 363039160, 53],
    [16.778400, 35.271610, 7399998550, 1000, 362792675, 53],
    [16.971506, 35.678753, 7399998550, 1000, 358671863, 53]
])

def unpaired_t_test(a_mean, a_std, a_n, b_mean, b_std, b_n):
    print("input: ", a_mean, a_std, a_n, b_mean, b_std, b_n)
    #s = math.sqrt((a_std**2 + b_std**2) / (a_n + b_n - 2 ))
    #t = (a_mean - b_mean) / math.sqrt(s**2 * (1 / a_n + 1 / b_n))
    #df = a_n + b_n - 4

    s = math.sqrt(a_std**2 / a_n + b_std**2 / b_n)
    df_top = (a_std**2 / a_n + b_std**2 / b_n)**2
    df_bottom = (a_std**2 / a_n)**2 / (a_n - 1) + (b_std**2 / b_n)**2 / (b_n - 1)
    df = df_top / df_bottom

    t = abs((a_mean - b_mean) / s)
    print(t, df)
    return 2 * (1 - scipy.stats.t.cdf(t, df))

def bootstrap(samples, n=100):
    mean = np.mean(samples)
    sampled_means = np.zeros((n, 1))
    for i in range(n):
        bootstrapped_samples = np.random.choice(samples, len(samples), replace=True)
        sampled_means[i] = np.mean(bootstrapped_samples)

    return mean, np.std(sampled_means, ddof=1)

X = draw_1[:, -2]   #sample_a[:, -2]
Y = draw_2[:, -2]   #sample_b[:, -2]

n_1 = len(X)
n_2 = len(Y)
mean_1, std_1 = bootstrap(X)
mean_2, std_2 = bootstrap(Y)

print(mean_1, std_1, mean_2, std_2)


print("bootstrapped p = {0:.10f}".format(unpaired_t_test(mean_1, np.sqrt(n_1)*std_1, n_1,
                                         mean_2, np.sqrt(n_2)*std_2, n_2)))
print("crude p = {0:.10f}".format(
    unpaired_t_test(np.mean(X),
                    np.sqrt(np.var(X)),
                    n_1,
                    np.mean(Y),
                    np.sqrt(np.var(Y)),
                    n_2)))

print(np.mean(X) * 1e-6,
      np.mean(X) * 1e-6,
      np.mean(X) * 1e-6)
print(np.sqrt(np.var(Y)) * 1e-6,
      np.sqrt(np.var(Y)) * 1e-6,
      np.sqrt(np.var(Y)) * 1e-6 )
#print("p = %.10f".format(unpaired_t_test(*control_variate_exp(), *control_variate_exp())))

plt.hist(X, 10)
plt.title("X sample")

plt.figure()
plt.hist(Y, 10)
plt.title("Y sample")
plt.show()