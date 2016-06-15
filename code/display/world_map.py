from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from scipy.spatial import Voronoi
from .custom_voronoi import voronoi_plot_no_points


class WorldMap:
    """
    Class implementing functionality for plotting data on a world map
    """
    def __init__(self, projection="cea", resolution="c"):
        self.map = Basemap(projection=projection, llcrnrlat=-90, urcrnrlat=90,
                           llcrnrlon=-180, urcrnrlon=180, lat_ts=20,
                           resolution=resolution)

    def add_points(self, points):
        """
        Adds points to the map

        Parameters
        ----------
        points : List of objectes of length 2 with long,lat. E.g. [(100,50), (105, 30)]
        """
        mapped_points = [self.map(x[0], x[1]) for x in points]
        longitudes = [x[0] for x in mapped_points]
        latitudes = [x[1] for x in mapped_points]

        self.map.plot(longitudes, latitudes, 'ro')#, latlon=True)

        # maybe useful in the future: curved lines:
        #self.map.drawgreatcircle(-50,45,50,60)

    def add_regions(self, region_list, marker_size=2):
        """
        Adds regions to the map

        Parameters
        ----------
        points : List of objectes with .longitude and .latitude propeties
        """
        #plot region centers
        mapped_points = [self.map(x.longitude, x.latitude) for x in region_list]
        longitudes = [x[0] for x in mapped_points]
        latitudes = [x[1] for x in mapped_points]

        self.map.plot(longitudes, latitudes, 'ro', markersize=marker_size)

        #plot neighbour connections
        connection_has_been_drawn = set()
        for region in region_list:
            for neighbour in region.neighbors:
                pair_tuple = (region.id, neighbour.id)
                if pair_tuple not in connection_has_been_drawn:
                    self.map.drawgreatcircle(region.longitude, region.latitude,
                                             neighbour.longitude, neighbour.latitude, color='k')
                    connection_has_been_drawn.add(pair_tuple)


 
    def add_voronoi(self, region_list):
        """
        Adds voronoi to the map

        Parameters
        ----------
        region_list : List of objectes with .longitude and .latitude propeties

        Returns
        -------
        None : mutates self.map
        """
        mapped_centers = [self.map(x.longitude, x.latitude) for x in region_list]
        vor = Voronoi(mapped_centers)
        voronoi_plot_no_points(vor)

    def show_plot(self, title="map", continent_color='coral', water_color='aqua', include_coast_lines=True):
        if include_coast_lines:
            self.map.drawcoastlines()
        
        self.map.fillcontinents(color=continent_color, lake_color=water_color)
        self.map.drawmapboundary(fill_color=water_color)
        plt.title(title)
        plt.show()


