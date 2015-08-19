"""
Based on http://www-cs-students.stanford.edu/~amitp/game-programming/grids/#relationships
"""
import numpy as np


class Map:

    def __init__(self, seed, generators):
        self.seed = seed
        self.generators = generators
        np.random.seed(seed)

        self.size = 1
        self.bbox = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.points = []  # used just for graph generator
        self.centers = []
        self.edges = []
        self.corners = []
        self.regions = []

    def generate(self):
        # Not sure this is the best pattern
        for generator in self.generators:
            generator(self)

    @property
    def land_corners(self):
        return [corner for corner in self.corners if not corner.water]


class Region:

    def __init__(self):
        self.centers = []

    @property
    def free_neighbors(self):
        neighbor_centers = []

        for center in self.centers:
            for neighbor in center.neighbors:
                if not neighbor.region and not neighbor.water:
                    neighbor_centers.append(neighbor)

        return neighbor_centers


BIOME_COLORS = {
    'BARE': '#bbbbbb',
    'BEACH': '#e9ddc7',
    'GRASSLAND': '#c4d4aa',
    'ICE': '#f0f0f0',
    'LAKE': '#96bff9',
    'MARSH': '#666666',
    'OCEAN': '#abceff',
    'SCORCHED': '#999999',
    'SHRUBLAND': '#c4ccbb',
    'SNOW': '#ffffff',
    'SUBTROPICAL_DESERT': '#c1b5a2',
    'TAIGA': '#ccd4bb',
    'TEMPERATE_DECIDUOUS_FOREST': '#b4c9a9',
    'TEMPERATE_DESERT': '#e4e8ca',
    'TEMPERATE_RAIN_FOREST': '#a4c4a8',
    'TROPICAL_RAIN_FOREST': '#9cbba9',
    'TROPICAL_SEASONAL_FOREST': '#a9cca4',
    'TUNDRA': '#777777',
}


class Center:

    def __init__(self, point):
        self.point = point
        self.neighbors = []  # list of Center
        self.borders = []  # list of Edge
        self.corners = []  # list of Corner
        self.region = None

        self.border = False  # at the edge of the map
        self.water = False  # lake or ocean
        self.ocean = False  # ocean
        self.coast = False  # land polygon touching an ocean
        self.elevation = 0  # 0.0 - 1.0. average of corners elevations
        self.moisture = 0  # 0.0 - 1.0
        self.biome = None

        # for export
        self.model = None

    @property
    def biome_color(self):
        return BIOME_COLORS[self.biome]


class Corner:

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


class Edge:

    def __init__(self, corners):
        self.centers = []  # 2-list of Center
        self.corners = corners  # 2-tuple of Corner
        self.midpoint = [
            (corners[0].point[0] + corners[1].point[0]) / 2,
            (corners[0].point[1] + corners[1].point[1]) / 2,
        ]

        self.border = False  # at the edge of the map
        self.river = 0  # 0 if no river, or volume of water in river
