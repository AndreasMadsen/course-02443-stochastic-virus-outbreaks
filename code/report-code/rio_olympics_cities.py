import _setup

import os.path as path
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import scipy.stats

from simulator import State, Simulator
from world import regions, routes

this_dir = path.dirname(path.realpath(__file__))

def plot_sir(sols, names, fig_name):
    n = len(sols)
    plt.subplots(figsize=(20,14))
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


        for simulation in sols[i-1].values():
            sol = np.asarray(simulation)

            p1, = plt.plot(sol[:, 0], color='SteelBlue', alpha=0.5, label='Susceptible')
            p2, = plt.plot(sol[:, 1], color='IndianRed', alpha=0.5, label='Infected')
            p3, = plt.plot(sol[:, 2], color='Olive', alpha=0.5, label='Removed')
            p4, = plt.plot(sol[:, 3], color='Gray', alpha=0.5, label='Total')

        plt.legend([p1, p2, p3, p4], ['S', 'I', 'R', 'T'])

    fig_save = path.join(this_dir, '../../report/plots/' + fig_name)
    print("saving figure {0}".format(fig_save))
    plt.savefig(fig_save,
                format='pdf', dpi=1000, bbox_inches='tight')


def execute_simulation(add_rio=False, ol_start=0, rio_length=18,
                       rio_visitors=380e3, n_simulations=5):

    sol_global = {}
    sol_rio = {}
    sol_moscow = {}
    sol_berlin = {}
    sol_beijing = {}
    sol_sydney = {}
    sol_new_york = {}
    for j in range(n_simulations):
        print("running simulation {0} / {1}".format(j + 1, n_simulations))
        state = State(regions, routes, verbose=True)
        state.set_outbreak('Rio De Janeiro', 1e3)#'Rio De Janeiro', 1000)
        sim = Simulator(state, transfer_prob=0.005, beta=2, gamma=0.5,
                        verbose=True)

        sol_global[j] = []
        sol_rio[j] = []
        sol_moscow[j] = []
        sol_berlin[j] = []
        sol_beijing[j] = []
        sol_sydney[j] = []
        sol_new_york[j] = []
        for i, state in enumerate(sim.run(iterations=180)):
            if i == ol_start and add_rio: # start outbreak x days before olympics
                sim.add_event(2560, days=rio_length, total_transfer=rio_visitors)

            sol_global[j].append(state.total_sir().as_tuple(total=True))
            sol_rio[j].append(state.region_sir[2560].as_tuple(total=True))
            sol_moscow[j].append(state.region_sir[4029].as_tuple(total=True))
            sol_berlin[j].append(state.region_sir[351].as_tuple(total=True))
            sol_beijing[j].append(state.region_sir[3364].as_tuple(total=True))
            sol_sydney[j].append(state.region_sir[3361].as_tuple(total=True))
            sol_new_york[j].append(state.region_sir[3797].as_tuple(total=True))

    if add_rio:
        fig_name = "rio-{0}-{1}-{2:d}.pdf".format(ol_start, rio_length,
                                                  int(rio_visitors))
    else:
        fig_name = "no_rio.pdf"

    plot_sir([sol_global, sol_rio, sol_new_york, sol_berlin,
              sol_moscow, sol_beijing, sol_sydney],
             ['Global', 'Rio De Janeiro', 'New York', 'Berlin',
              'Moscow', 'Beijing', 'Sydney'], fig_name)

    global_values = sol_global.values()
    peak_times_global = [np.argmax([x[1] for x in y])
                         for y in global_values]
    peak_amount_global = [y[peak][1]
                          for peak, y in zip(peak_times_global, global_values)]


    peak_times_rio = [np.argmax([x[1] for x in y])
                      for y in  sol_rio.values()]
    peak_times_new_york = [np.argmax([x[1] for x in y])
                           for y in  sol_new_york.values()]
    peak_times_berlin = [np.argmax([x[1] for x in y])
                         for y in  sol_berlin.values()]
    peak_times_moscow = [np.argmax([x[1] for x in y])
                         for y in  sol_moscow.values()]
    peak_times_beijing = [np.argmax([x[1] for x in y])
                          for y in  sol_beijing.values()]
    peak_times_sydney = [np.argmax([x[1] for x in y])
                         for y in  sol_sydney.values()]

    t_deviations = scipy.stats.t.ppf(0.975, len(peak_times_rio)-1)
    return [(np.mean(peak_times_global), t_deviations * np.std(peak_times_global, ddof=1)),
            (np.mean(peak_amount_global), t_deviations * np.std(peak_amount_global, ddof=1)),
            (np.mean(peak_times_rio), t_deviations * np.std(peak_times_rio, ddof=1)),
            (np.mean(peak_times_new_york), t_deviations * np.std(peak_times_new_york, ddof=1)),
            (np.mean(peak_times_berlin), t_deviations * np.std(peak_times_berlin, ddof=1)),
            (np.mean(peak_times_moscow), t_deviations * np.std(peak_times_moscow, ddof=1)),
            (np.mean(peak_times_beijing), t_deviations * np.std(peak_times_beijing, ddof=1)),
            (np.mean(peak_times_sydney), t_deviations * np.std(peak_times_sydney, ddof=1))
           ]

if __name__ == "__main__":
    names = ["Peak time Global", "Peak amount Global",
             "Peak time Rio", "Peak time New York", "Peak time Berlin",
             "Peak time Moscow", "Peak time Beijing", "Peak time Sydney"]
    res_with_ol = execute_simulation(True, n_simulations=10)
    res_without_ol = execute_simulation(False, n_simulations=10)

    latex_table = "\\begin{tabular}[H]{c | c | c |}"
    latex_table += "\nObservation & With OL & Without OL \\\\ \\hline "
    latex_table += "\n {0} & ${1:.2f}\\pm {2:.2f}$ & ${3:.2f} \\pm {4:.2f}$".format(
        names[0], res_with_ol[0][0], res_with_ol[0][1],
        res_without_ol[0][0], res_without_ol[0][1]
        )
    for i in range(1, len(names)):
        latex_table += "\\\\ \n {0} & ${1:.2f}\\pm {2:.2f}$ & ${3:.2f} \\pm {4:.2f}$".format(
            names[i], res_with_ol[i][0], res_with_ol[i][1],
            res_without_ol[i][0], res_without_ol[i][1]
        )
    latex_table += "\n\\end{tabular}"

    table_save = path.join(this_dir, '../../report/tables/result.tex')
    tex_file = open(table_save, 'w')
    tex_file.write(latex_table)
    tex_file.close()






