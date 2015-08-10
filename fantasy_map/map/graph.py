"""
Based on http://www-cs-students.stanford.edu/~amitp/game-programming/grids/#relationships
"""
import numpy as np

BIOME_COLORS = {
    'OCEAN': '#abceff',
    'LAKE': '#1b6ee3',
    'ICE': '#f0f0f0',
    'MARSH': '#666666',
    'BEACH': '#e9ddc7',
    'SNOW': '#ffffff',
    'TUNDRA': '#777777',
    'BARE': '#bbbbbb',
    'SCORCHED': '#999999',
    'TAIGA': '#ccd4bb',
    'SHRUBLAND': '#c4ccbb',
    'TEMPERATE_DESERT': '#e4e8ca',
    'TEMPERATE_RAIN_FOREST': '#a4c4a8',
    'TEMPERATE_DECIDUOUS_FOREST': '#b4c9a9',
    'GRASSLAND': '#c4d4aa',
    'TROPICAL_RAIN_FOREST': '#9cbba9',
    'TROPICAL_SEASONAL_FOREST': '#a9cca4',
    'SUBTROPICAL_DESERT': '#c1b5a2'
}


class Center(object):

    def __init__(self, point):
        self.point = point
        self.neighbors = []  # list of Center
        self.borders = []  # list of Edge
        self.corners = []  # list of Corner

        self.border = False  # at the edge of the map
        self.water = False  # lake or ocean
        self.ocean = False  # ocean
        self.coast = False  # land polygon touching an ocean
        self.elevation = 0  # 0.0 - 1.0. average of corners elevations
        self.moisture = 0  # 0.0 - 1.0
        self.biome = None

    @property
    def biome_color(self):
        return BIOME_COLORS[self.biome]

    def lightnings(self):
        # Return light level for each edge (0-1).
        light_vector = np.array([1, 1, 1])
        light_vector = light_vector / np.linalg.norm(light_vector)
        output = []

        for edge in self.borders:
            c1 = edge.corners[0]
            c2 = edge.corners[1]

            v1 = np.array([
                self.point[0],
                self.point[1],
                self.elevation
            ])

            v2 = np.array([
                c1.point[0],
                c1.point[1],
                c1.elevation
            ])

            v3 = np.array([
                c2.point[0],
                c2.point[1],
                c2.elevation
            ])

            normal = np.cross(v2 - v1, v3 - v1)
            if normal[2] < 0:
                normal *= -1

            normal = normal / np.linalg.norm(normal)
            light = 0.5 + 0.5 * np.dot(normal, light_vector)
            output.append(light)

        return output


class Corner(object):

    def __init__(self, point):
        self.point = point
        self.touches = []  # list of Center
        self.protrudes = []  # list of Edge
        self.adjacent = []  # list of Corner

        self.border = False  # at the edge of the map
        self.water = False  # lake or ocean
        self.ocean = False  # all touches are ocean
        self.coast = False  # touches ocean and land polygons
        self.elevation = 0  # 0.0 - 1.0

        self.river = 0  # 0 if no river, or volume of water in river
        self.downslope = None  # Corner, pointer to adjacent corner most downhill
        self.downslope_edge = None  # Edge between this Corner and downslope
        self.moisture = 0  # 0.0 - 1.0


class Edge(object):

    def __init__(self, corners):
        self.centers = []  # 2-list of Center
        self.corners = corners  # 2-tuple of Corner
        self.midpoint = [
            (corners[0].point[0] + corners[1].point[0]) / 2,
            (corners[0].point[1] + corners[1].point[1]) / 2,
        ]

        self.border = False  # at the edge of the map
        self.river = 0  # 0 if no river, or volume of water in river
