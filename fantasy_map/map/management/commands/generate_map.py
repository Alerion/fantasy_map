"""
Inspired by http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/

Used:
    - https://stackoverflow.com/questions/20515554/colorize-voronoi-diagram/20678647#20678647
"""
from __future__ import division

import collections
from pprint import pprint
from scipy.spatial import Delaunay, KDTree, delaunay_plot_2d, Voronoi, voronoi_plot_2d
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate new map'

    def handle(self, *args, **options):
        points = np.random.random((6, 2))
        plt.figure(figsize=(10, 10))
        ax = plt.subplot(1, 1, 1)

        for point in points:
            ax.plot([point[0]], [point[1]], 'o')

        vor = Voronoi(points)
        voronoi_plot_2d(vor)

        # vertices, regions = voronoi_finite_polygons_2d(vor)
        # for region in regions:
        #     polygon = vertices[region]
        #     p = matplotlib.patches.Polygon(polygon, facecolor=(1, 1, 1))
        #     ax.add_patch(p)

        ax.plot(points[:, 0], points[:, 1], '.')

        centers, edges, corners = polygons(points)

        for center in centers:
            p = matplotlib.patches.Polygon([c.point for c in center.corners], facecolor=(1, 1, 1))
            ax.add_patch(p)

            # for edge in center.borders:
            #     ax.plot(
            #         [center.point[0], edge.midpoint[0]],
            #         [center.point[1], edge.midpoint[1]],
            #         'k--')

            # for neigh in center.neighbors:
            #     ax.plot(
            #         [center.point[0], neigh.point[0]],
            #         [center.point[1], neigh.point[1]],
            #         'k:')

        for corner in corners:
            ax.plot([corner.point[0]], [corner.point[1]], '.')

        # for edge in edges:
        #     ax.plot(
        #         [edge.corners[0].point[0], edge.corners[1].point[0]],
        #         [edge.corners[0].point[1], edge.corners[1].point[1]],
        #         'k-')

        #     if len(edge.centers) == 2:
        #         ax.plot(
        #             [edge.centers[0].point[0], edge.centers[1].point[0]],
        #             [edge.centers[0].point[1], edge.centers[1].point[1]],
        #             'k--')

        plt.axis([-0.05, 1.05, -0.05, 1.05])
        plt.show()


def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.

    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.

    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.

    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return np.asarray(new_vertices), new_regions


def key(p1, p2=None):
    if p2 is None:
        return tuple(p1)
    return tuple(sorted([tuple(p1), tuple(p2)]))


def polygons(points):
    '''
    Returns the voronoi polygon for each input point.

    :param points: shape (n, 2)
    :rtype: list of n polygons where each polygon is an array of vertices
    '''
    vertices, regions = voronoi_finite_polygons_2d(Voronoi(points))

    cells = []
    for region in regions:
        edges = []
        for i in range(len(region) - 1):
            edges.append((region[i], region[i + 1]))
        edges.append((region[-1], region[0]))
        cells.append(edges)

    centers = {}
    corners = {}
    edges = {}

    for index, point in enumerate(points):
        center = Center(index, point)
        centers[key(point)] = center

    for index, vertice in enumerate(vertices):
        corner = Corner(index, vertice)
        corners[key(vertice)] = corner

    for point_index, edge_indices in enumerate(cells):
        point = points[point_index]
        center = centers[key(point)]

        for p1_index, p2_index in edge_indices:
            p1, p2 = vertices[p1_index], vertices[p2_index]
            if key(p1, p2) not in edges:
                corner1 = corners[key(p1)]
                corner2 = corners[key(p2)]
                edge = Edge(index, (corner1, corner2))
                corner1.protrudes.append(edge)
                corner2.protrudes.append(edge)
                corner1.adjacent.append(corner1)
                corner2.adjacent.append(corner2)
                edges[key(p1, p2)] = edge
            else:
                edge = edges[key(p1, p2)]

            center.borders.append(edge)
            edge.centers.append(center)

    for point_index, vertice_indeces in enumerate(regions):
        point = points[point_index]
        center = centers[key(point)]

        for vertice_index in vertice_indeces:
            vertice = vertices[vertice_index]
            corner = corners[key(vertice)]
            center.corners.append(corner)
            corner.touches.append(center)

    for edge in edges.values():
        assert 1 <= len(edge.centers) <= 2
        if len(edge.centers) == 1:
            edge.centers[0].border = True
        else:
            edge.centers[0].neighbors.append(edge.centers[1])
            edge.centers[1].neighbors.append(edge.centers[0])

    return centers.values(), edges.values(), corners.values()


class Center(object):

    def __init__(self, index, point):
        self.index = index
        self.point = point
        self.neighbors = []  # list of Center
        self.borders = []  # list of Edge
        self.corners = []  # list of Corner

        self.border = False  # at the edge of the map


class Corner(object):

    def __init__(self, index, point):
        self.index = index
        self.point = point
        self.touches = []  # list of Center
        self.protrudes = []  # list of Edge
        self.adjacent = []  # list of Corner


class Edge(object):

    def __init__(self, index, corners):
        self.index = index
        self.corners = corners  # 2-tuple of Corner
        self.midpoint = [
            (corners[0].point[0] + corners[1].point[0]) / 2,
            (corners[0].point[1] + corners[1].point[1]) / 2,
        ]
        self.centers = []  # 2-list of Center
