"""code taken from scipy/spatial/_plotutils.py and modified to plot voronoi withouth centers"""

import numpy as np
from scipy._lib.decorator import decorator as _decorator
from scipy.spatial._plotutils import _held_figure, _adjust_bounds

@_held_figure
def voronoi_plot_no_points(vor, ax=None):
    """
    Plot the given Voronoi diagram in 2-D
    Parameters
    ----------
    vor : scipy.spatial.Voronoi instance
        Diagram to plot
    ax : matplotlib.axes.Axes instance, optional
        Axes to plot on
    Returns
    -------
    fig : matplotlib.figure.Figure instance
        Figure for the plot
    See Also
    --------
    Voronoi
    Notes
    -----
    Requires Matplotlib.
    """
    if vor.points.shape[1] != 2:
        raise ValueError("Voronoi diagram is not 2-D")

    ax.plot(vor.points[:, 0], vor.points[:, 1], 'o')
    #ax.plot(vor.vertices[:,0], vor.vertices[:,1], 'o')

    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            ax.plot(vor.vertices[simplex, 0], vor.vertices[simplex, 1], 'k-')

    ptp_bound = vor.points.ptp(axis=0)

    center = vor.points.mean(axis=0)
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.any(simplex < 0):
            i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

            t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[pointidx].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[i] + direction * ptp_bound.max()

            ax.plot([vor.vertices[i, 0], far_point[0]],
                    [vor.vertices[i, 1], far_point[1]], 'k--')

    _adjust_bounds(ax, vor.points)

    return ax.figure
