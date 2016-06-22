
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial import Voronoi
import numpy as np
import math

from ._custom_voronoi import voronoi_plot_no_points

class WorldMap:
    """
    Class implementing functionality for plotting data on a world map
    """

    def __init__(self, projection="cea", resolution="c",
                 continent_color='coral', water_color='aqua'):

        # Setup figure and basemap
        self.fig, self.ax = plt.subplots(figsize=(20,14))
        self.map = Basemap(projection=projection, llcrnrlat=-90, urcrnrlat=90,
                           llcrnrlon=-180, urcrnrlon=180, lat_ts=20,
                           resolution=resolution, ax=self.ax)

        # Draw world map
        self.map.drawcoastlines(zorder=1)
        self.map.fillcontinents(color=continent_color, lake_color=water_color, zorder=1)
        self.map.drawmapboundary(fill_color=water_color, zorder=1)

        self.ani = None

    def add_airports(self, regions):
        """
        Adds points to the map

        Parameters
        ----------
        regions : Region dict with .longitude and .latitude propeties
        """
        region_ids = [region_id for region_id in regions.keys()]

        longitudes = np.fromiter(
            (regions[id].longitude for id in region_ids),
            dtype='float'
        )
        latitudes = np.fromiter(
            (regions[id].latitude for id in region_ids),
            dtype='float'
        )

        x, y = self.map(longitudes, latitudes)
        self.map.scatter(x, y, zorder=2, s=2, lw=0, c='k')

    def add_airport_connections(self, regions):
        """ Adds connections between airports on the map

        Parameters
        ---------
        regions : Region dict
        """

        connection_has_been_drawn = set()

        for region in regions.values():
            for destination in (x.destination for x in region.airlines):

                # Prevent the same connection from being drawn twice
                edge_id = (region.id, destination.id)
                if region.id > destination.id:
                    edge_id = (destination.id, destination.id)

                if edge_id in connection_has_been_drawn:
                    continue

                connection_has_been_drawn.add(edge_id)

                # Draw connection
                self.map.drawgreatcircle(
                    region.longitude, region.latitude,
                    destination.longitude, destination.latitude,
                    color='k', ls='--', alpha=0.1)


    def _infected_rate(self, sir):
        pop = sir.susceptible + sir.infected + sir.removed
        if pop == 0: return 0
        return sir.infected / pop

    def _getinfected(self, simulator, region_ids):
        simulator.step()
        region_sir = simulator.state.region_sir

        return np.fromiter(
            (self._infected_rate(region_sir[id]) for id in region_ids),
            dtype='float32'
        )

    def _update_plot(self, i, simulator, region_ids, scat, time):
        scat.set_array(self._getinfected(simulator, region_ids))
        time.set_text('t = %d' % (i + 1))
        return scat, time

    def animate(self, simulator, frames=365, fps=1 / 20, max_infected=1):
        """
        Animates a simulator which implements a step function

        Parameters
        ----------
        simulator : Simulator object that implements a step function.
        frames    : number of frames/steps to compute (default 300)
        fps       : frames pr second (default 1/20)
        """
        # The order of the region sequence is not necessary consistent,
        # so create an id list now, which will determin the ordering.
        regions = simulator.state.regions
        region_ids = [region_id for region_id in regions.keys()]

        # Pre compute longitude and latitudes, they are not updated
        longitudes = np.fromiter(
            (regions[id].longitude for id in region_ids),
            dtype='float'
        )
        latitudes = np.fromiter(
            (regions[id].latitude for id in region_ids),
            dtype='float'
        )
        sizes = np.fromiter(
            (math.sqrt(simulator.state.region_sir[id].total_pop) \
            for id in simulator.state.region_sir),
            dtype='float'
        )
        sizes = 5 + (sizes - min(sizes)) / (max(sizes)-min(sizes)) * 50
        x_map, y_map = self.map(longitudes, latitudes)

        # Initialize scatter plot, which will be updated in animation
        scat = self.map.scatter(
            x_map, y_map, c=self._getinfected(simulator, region_ids),
            s=sizes, lw=0, zorder=2,
            vmin=0, vmax=max_infected, cmap='summer'
        )

        self.map.colorbar(scat)

        time = self.ax.text(*self.map(-170, -65), s='t = 0', fontsize=12)

        # Create animation object
        self.ani = animation.FuncAnimation(
            self.fig, self._update_plot,
            frames=frames, interval=1 / fps,
            fargs=(simulator, region_ids, scat, time),
            repeat=False
        )

    def scatter_infections(self, state, max_infected=1, time=0):
        """Plots a scatter plot on the map of the current state

        Parameters
        ---------
        state : current state
        max_infected : upper bound on the colorbar used for the scatter plot

        Returns
        -------
        None : Mutates the BaseMap object
        """
        regions = state.regions
        region_ids = [region_id for region_id in regions.keys()]

        # Pre compute longitude and latitudes, they are not updated
        longitudes = np.fromiter(
            (regions[id].longitude for id in region_ids),
            dtype='float'
        )
        latitudes = np.fromiter(
            (regions[id].latitude for id in region_ids),
            dtype='float'
        )
        sizes = np.fromiter(
            (math.sqrt(state.region_sir[id].total_pop) \
            for id in state.region_sir),
            dtype='float'
        )
        sizes = 5 + (sizes - min(sizes)) / (max(sizes)-min(sizes)) * 50
        x_map, y_map = self.map(longitudes, latitudes)

        scat = self.map.scatter(
            x_map, y_map, c=[self._infected_rate(x) for x in state.region_sir.values()],
            s=sizes, lw=0, zorder=2,
            vmin=0, vmax=max_infected, cmap='summer'
        )

        self.map.colorbar(scat)
        self.ax.text(*self.map(-170, -65), s='t = {0}'.format(time),
            fontsize=12)

    def add_neighbours(self, regions):
        """
        Adds regions to the map

        Parameters
        ----------
        regions : List of objectes with .longitude and .latitude propeties
        """
        # Plot neighbour connections
        connection_has_been_drawn = set()
        for region in regions:
            for neighbour in region.neighbors:

                # Prevent the same connection from being drawn twice
                edge_id = (region.id, neighbour.id)
                if region.id > neighbour.id:
                    edge_id = (neighbour.id, region.id)

                if edge_id in connection_has_been_drawn:
                    continue

                connection_has_been_drawn.add(edge_id)

                # Draw connection
                self.map.drawgreatcircle(
                    region.longitude, region.latitude,
                    neighbour.longitude, neighbour.latitude,
                    color='k', alpha=0.5)

    def add_voronoi(self, regions):
        """
        Adds voronoi to the map

        Parameters
        ----------
        regions : Region dict with .longitude and .latitude propeties

        Returns
        -------
        None : mutates self.map
        """
        mapped_centers = [self.map(x.longitude, x.latitude) for x in regions.values()]
        vor = Voronoi(mapped_centers)
        voronoi_plot_no_points(vor, ax=self.ax)

    def show(self):
        if self.ani is not None:
            plt.show(self.ani)
        else:
            plt.show()

    def save_fig(self, name, format='pdf', dpi=1000):
        if self.ani is not None:
            plt.savefig(name, format=format,
                        dpi=dpi, bbox_inches='tight')
        else:
            plt.savefig(name, format=format, dpi=dpi,
                        bbox_inches='tight')