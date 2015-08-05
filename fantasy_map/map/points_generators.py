import numpy as np

from .voronoi import voronoi_finite_polygons


class RandomPoints(object):

    def __init__(self, points_number):
        self.points_number = points_number

    def generate_points(self, map_obj):
        map_obj.points = np.random.random((self.points_number, 2))


class RelaxedPoints(object):
    """
    Improve the random set of points with Lloyd Relaxation
    """

    def __init__(self, points_number, lloyd_iterations=2):
        self.points_number = points_number
        self.lloyd_iterations = lloyd_iterations

    def generate_points(self, map_obj):
        points = np.random.random((self.points_number, 2))

        for _ in range(self.lloyd_iterations):
            regions = voronoi_finite_polygons(points, bbox=map_obj.bbox)
            points = []
            for region in regions:
                points.append(region.mean(axis=0))  # get centroid

        map_obj.points = points
