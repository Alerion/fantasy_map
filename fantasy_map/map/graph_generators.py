from .graph import Center, Edge, Corner
from .voronoi import voronoi_finite_polygons


def key(p1, p2=None):
    if p2 is None:
        return tuple(p1)
    return tuple(sorted([tuple(p1), tuple(p2)]))


class VoronoiGraph(object):

    def generate_graph(self, map_obj):
        points = map_obj.points
        regions = voronoi_finite_polygons(points, bbox=map_obj.bbox)

        centers = {}
        corners = {}
        edges = {}

        for point in points:
            centers[key(point)] = Center(point)

        region_edges = []
        for region in regions:
            cell_edges = []
            for i in range(len(region) - 1):
                cell_edges.append((region[i], region[i + 1]))

            region_edges.append(cell_edges)

            for vertice in region:
                if key(vertice) not in corners:
                    corner = Corner(vertice)
                    corner.border = (
                        vertice[0] == 0 or vertice[0] == 1 or vertice[1] == 0 or vertice[1] == 1
                    )
                    corners[key(vertice)] = corner

        for point_index, cell_edges in enumerate(region_edges):
            point = points[point_index]
            center = centers[key(point)]

            for p1, p2 in cell_edges:
                if key(p1, p2) not in edges:
                    corner1 = corners[key(p1)]
                    corner2 = corners[key(p2)]
                    edge = Edge((corner1, corner2))
                    corner1.protrudes.append(edge)
                    corner2.protrudes.append(edge)
                    corner1.adjacent.append(corner1)
                    corner2.adjacent.append(corner2)
                    edge.border = corner1.border and corner2.border
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
