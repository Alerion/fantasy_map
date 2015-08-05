from scipy.spatial import Voronoi
import numpy as np

from .voronoi import voronoi_finite_polygons_2d


class RandomPoints(object):

    def __init__(self, points_number):
        self.points_number = points_number

    def __call__(self, map_obj):
        map_obj.points = np.random.random((self.points_number, 2))


class RelaxedPoints(object):
    """
    Improve the random set of points with Lloyd Relaxation
    """

    def __init__(self, points_number, lloyd_iterations=2):
        self.points_number = points_number
        self.lloyd_iterations = lloyd_iterations

    def __call__(self, map_obj):
        points = np.random.random((self.points_number, 2))

        for _ in range(self.lloyd_iterations):
            _, regions = voronoi_finite_polygons_2d(points)
            points = []
            for region in regions:
                points.append(region.mean(axis=0))

        map_obj.points = points
