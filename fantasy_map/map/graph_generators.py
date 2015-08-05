from scipy.spatial import Voronoi
import numpy as np

from .graph import Center, Edge, Corner


def key(p1, p2=None):
    if p2 is None:
        return tuple(p1)
    return tuple(sorted([tuple(p1), tuple(p2)]))


class VoronoiGenerator(object):

    def __init__(self, points_number):
        self.points_number = points_number

    def __call__(self, map_obj):
        points = np.random.random((self.points_number, 2))
        vertices, regions = self._voronoi_finite_polygons_2d(points)

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

        map_obj.centers = centers.values()
        map_obj.edges = edges.values()
        map_obj.corners = corners.values()

    def _voronoi_finite_polygons_2d(self, points, radius=None):
        """
        Reconstruct infinite voronoi regions in a 2D diagram to finite
        regions.

        From here: https://stackoverflow.com/questions/20515554/colorize-voronoi-diagram/20678647
        """
        vor = Voronoi(points)

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
