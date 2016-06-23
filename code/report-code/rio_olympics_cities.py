import _setup

import os.path as path
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import scipy.stats
import math

from simulator import State, Simulator
from world import regions, routes
import sir

this_dir = path.dirname(path.realpath(__file__))

def plot_sir(sols, names, fig_name):
    n = len(sols)
    plt.subplots(figsize=(10,12))
    for i in range(1, n+1):
        # share x-axis
        if i == 1:
            ax = plt.subplot(n * 100 + 10 + i)
        else:
            ax = plt.subplot(n * 100 + 10 + i, sharex=ax)

        # hide x ticks except for last
        if i != n:
            plt.setp(ax.get_xticklabels(), visible=False)

        ax.set_title(names[i-1])


        for simulation in sols[i-1]:
            sol = np.asarray(simulation)

            p1, = plt.plot(sol[:, 0], color='SteelBlue', alpha=0.5, label='Susceptible')
            p2, = plt.plot(sol[:, 1], color='IndianRed', alpha=0.5, label='Infected')
            p3, = plt.plot(sol[:, 2], color='Olive', alpha=0.5, label='Removed')
            p4, = plt.plot(sol[:, 3], color='Gray', alpha=0.5, label='Total')

        plt.legend([p1, p2, p3, p4], ['S', 'I', 'R', 'T'])

    fig_save = path.join(this_dir, '../../report/plots/' + fig_name)
    print("saving figure {0}".format(fig_save))
    plt.savefig(fig_save,
                format='pdf', bbox_inches='tight')


def control_variate_conf(y, x, verbose=False):

    if verbose:
        print(np.corrcoef(x, y))

    c = -np.cov(x, y)[1, 0] / np.var(x, ddof=1)
    z = y + c * (x - np.mean(x))

    std_z = np.std(z, ddof=2)

    n = len(z)
    confidence = scipy.stats.t.ppf(0.975, n - 1) * std_z / math.sqrt(n)

    return confidence

def execute_simulation(add_rio=False, ol_start=0, rio_length=18,
                       rio_visitors=380e3, n_simulations=5):

    sol_global = []
    sol_rio = []
    sol_moscow = []
    sol_berlin = []
    sol_beijing = []
    sol_sydney = []
    sol_new_york = []
    params = {}
    params['global'] = []
    params['rio'] = []
    params['moscow'] = []
    params['berlin'] = []
    params['beijing'] = []
    params['sydney'] = []
    params['new'] = []
    for j in range(n_simulations):
        print("running simulation {0} / {1}".format(j + 1, n_simulations))
        state = State(regions, routes, verbose=True)
        state.set_outbreak('Rio De Janeiro', 1e3)#'Rio De Janeiro', 1000)
        sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5,
                        verbose=True)

        sol_global.append([])
        sol_rio.append([])
        sol_moscow.append([])
        sol_berlin.append([])
        sol_beijing.append([])
        sol_sydney.append([])
        sol_new_york.append([])
        state_list = []
        for i, state in enumerate(sim.run(iterations=120)):
            state_list.append(state)
            if i == ol_start and add_rio: # start outbreak x days before olympics
                sim.add_event(2560, days=rio_length, total_transfer=rio_visitors)

            sol_global[j].append(state.total_sir().as_tuple(total=True))
            sol_rio[j].append(state.region_sir[2560].as_tuple(total=True))
            sol_moscow[j].append(state.region_sir[4029].as_tuple(total=True))
            sol_berlin[j].append(state.region_sir[351].as_tuple(total=True))
            sol_beijing[j].append(state.region_sir[3364].as_tuple(total=True))
            sol_sydney[j].append(state.region_sir[3361].as_tuple(total=True))
            sol_new_york[j].append(state.region_sir[3797].as_tuple(total=True))

        params['global'].append(sir.ParameterEstimator(
            iter([x.total_sir() for x in state_list]), method='max').beta)
        params['rio'].append(sir.ParameterEstimator(
            iter([x.region_sir[2560] for x in state_list]), method='max').beta)
        params['moscow'].append(sir.ParameterEstimator(
            iter([x.region_sir[4029] for x in state_list]), method='max').beta)
        params['berlin'].append(sir.ParameterEstimator(
            iter([x.region_sir[351] for x in state_list]), method='max').beta)
        params['beijing'].append(sir.ParameterEstimator(
            iter([x.region_sir[3364] for x in state_list]), method='max').beta)
        params['sydney'].append(sir.ParameterEstimator(
            iter([x.region_sir[3361] for x in state_list]), method='max').beta)
        params['new'].append(sir.ParameterEstimator(
            iter([x.region_sir[2560] for x in state_list]), method='max').beta)

    if add_rio:
        fig_name = "rio-{0}-{1}-{2:d}.pdf".format(ol_start, rio_length,
                                                  int(rio_visitors))
    else:
        fig_name = "no_rio.pdf"

    plot_sir([sol_global, sol_rio, sol_new_york, sol_berlin,
              sol_moscow, sol_beijing, sol_sydney],
             ['Global', 'Rio De Janeiro', 'New York', 'Berlin',
              'Moscow', 'Beijing', 'Sydney'], fig_name)

    # estimate means and variance
    global_values = sol_global
    peak_times_global = [np.argmax([x[1] for x in y])
                         for y in global_values]
    peak_amount_global = [y[peak][1]
                          for peak, y in zip(peak_times_global, global_values)]


    peak_times_rio = [np.argmax([x[1] for x in y])
                      for y in  sol_rio]
    peak_times_new_york = [np.argmax([x[1] for x in y])
                           for y in  sol_new_york]
    peak_times_berlin = [np.argmax([x[1] for x in y])
                         for y in  sol_berlin]
    peak_times_moscow = [np.argmax([x[1] for x in y])
                         for y in  sol_moscow]
    peak_times_beijing = [np.argmax([x[1] for x in y])
                          for y in  sol_beijing]
    peak_times_sydney = [np.argmax([x[1] for x in y])
                         for y in  sol_sydney]

    t_deviations = scipy.stats.t.ppf(0.975, len(peak_times_rio)-1)

    # estimate variance with control variates
    amount_global_control_conf = control_variate_conf(peak_amount_global, params['global'])
    time_global_control_conf = control_variate_conf(peak_times_global, params['global'])
    time_rio_control_conf = control_variate_conf(peak_times_rio, params['rio'])
    time_new_york_control_conf = control_variate_conf(peak_times_new_york, params['new'])
    time_berlin_control_conf = control_variate_conf(peak_times_berlin, params['berlin'])
    time_moscow_control_conf = control_variate_conf(peak_times_moscow, params['moscow'])
    time_beijing_control_conf = control_variate_conf(peak_times_beijing, params['beijing'])
    time_sydney_control_conf = control_variate_conf(peak_times_sydney, params['sydney'])

    return [(np.mean(peak_amount_global),
             t_deviations * np.std(peak_amount_global, ddof=1) / math.sqrt(n_simulations),
             amount_global_control_conf),
            (np.mean(peak_times_global),
             t_deviations * np.std(peak_times_global, ddof=1) / math.sqrt(n_simulations),
             time_global_control_conf),
            (np.mean(peak_times_rio),
             t_deviations * np.std(peak_times_rio, ddof=1) / math.sqrt(n_simulations),
             time_rio_control_conf),
            (np.mean(peak_times_new_york),
             t_deviations * np.std(peak_times_new_york, ddof=1) / math.sqrt(n_simulations),
             time_new_york_control_conf),
            (np.mean(peak_times_berlin),
             t_deviations * np.std(peak_times_berlin, ddof=1) / math.sqrt(n_simulations),
             time_berlin_control_conf),
            (np.mean(peak_times_moscow),
             t_deviations * np.std(peak_times_moscow, ddof=1) / math.sqrt(n_simulations),
             time_moscow_control_conf),
            (np.mean(peak_times_beijing),
             t_deviations * np.std(peak_times_beijing, ddof=1) / math.sqrt(n_simulations),
             time_beijing_control_conf),
            (np.mean(peak_times_sydney),
             t_deviations * np.std(peak_times_sydney, ddof=1) / math.sqrt(n_simulations),
             time_sydney_control_conf)
           ]

if __name__ == "__main__":
    names = ["Peak amount Global", "Peak time Global",
             "Peak time Rio", "Peak time New York", "Peak time Berlin",
             "Peak time Moscow", "Peak time Beijing", "Peak time Sydney"]
    n_sim = 10
    res_with_ol = execute_simulation(True, n_simulations=n_sim)
    res_without_ol = execute_simulation(False, n_simulations=n_sim)

    latex_table = "\\begin{tabular}[H]{c | c | c}"
    latex_table += "\nObservation & With OL & Without OL \\\\ \\hline "
    latex_table += "\n {0} [million]& ${1:.1f}\\pm {2:.2f} ({3:.2f})$ & ${4:.1f} \\pm {5:.2f} ({6:.2f})$".format(
        names[0], res_with_ol[0][0] / 1e6, res_with_ol[0][1] / 1e6, res_with_ol[0][2] / 1e6,
        res_without_ol[0][0] / 1e6, res_without_ol[0][1] / 1e6, res_without_ol[0][2] / 1e6
        )
    for i in range(1, len(names)):
        latex_table += "\\\\ \n {0} & ${1:.1f}\\pm {2:.2f}( {3:.2f})$ & ${4:.1f} \\pm {5:.2f} ({6:.2f})$".format(
            names[i], res_with_ol[i][0], res_with_ol[i][1], res_with_ol[i][2],
            res_without_ol[i][0], res_without_ol[i][1], res_without_ol[i][2],
        )
    latex_table += "\n\\end{tabular}"

    table_save = path.join(this_dir, '../../report/tables/result.tex')
    tex_file = open(table_save, 'w')
    tex_file.write(latex_table)
    tex_file.close()
