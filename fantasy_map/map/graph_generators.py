from .graph import Center, Edge, Corner
from .voronoi import voronoi_finite_polygons_2d


def key(p1, p2=None):
    if p2 is None:
        return tuple(p1)
    return tuple(sorted([tuple(p1), tuple(p2)]))


class VoronoiGraph(object):

    def __call__(self, map_obj):
        points = map_obj.points
        vertices, regions = voronoi_finite_polygons_2d(points)

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

        for point_index, cell_edges in enumerate(cells):
            point = points[point_index]
            center = centers[key(point)]

            for p1, p2 in cell_edges:
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

        for point_index, region_vertices in enumerate(regions):
            point = points[point_index]
            center = centers[key(point)]

            for vertice in region_vertices:
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
