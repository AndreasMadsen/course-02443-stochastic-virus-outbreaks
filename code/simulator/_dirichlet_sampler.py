
import numpy as np
import scipy.stats

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

def sample_dirichlet(p_list, n):
    """Sample groups of people from a population of size n with each group
    getting on average n * p_list[i]

    Parameters
    ----------
    p_list : properbility in a binomial context for getting a person
    n : population size
    """
    if len(p_list) == 0:
        return []

    if sum(p_list) > 1:
        raise ValueError('sum of p_list excited 1, sum = %f' % sum(p_list))

    alpha = np.fromiter(_calc_alpha(p_list, n), dtype='float')
    parts = scipy.stats.dirichlet.rvs(alpha)[0]
    people = (parts * n).astype('int').tolist()

    # Setup a people list with zeros, in case the properbility was zero
    people_zero = []
    people_iter = iter(people)
    for p in p_list:
        people_zero.append(next(people_iter) if p > 0 else 0)

    return people_zero
