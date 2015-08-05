"""
Based on http://www-cs-students.stanford.edu/~amitp/game-programming/grids/#relationships
"""


class Center(object):

    def __init__(self, point):
        self.point = point
        self.neighbors = []  # list of Center
        self.borders = []  # list of Edge
        self.corners = []  # list of Corner

        self.border = False  # at the edge of the map


class Corner(object):

    def __init__(self, point):
        self.point = point
        self.touches = []  # list of Center
        self.protrudes = []  # list of Edge
        self.adjacent = []  # list of Corner

        self.border = False  # at the edge of the map


class Edge(object):

    def __init__(self, corners):
        self.centers = []  # 2-list of Center
        self.corners = corners  # 2-tuple of Corner
        self.midpoint = [
            (corners[0].point[0] + corners[1].point[0]) / 2,
            (corners[0].point[1] + corners[1].point[1]) / 2,
        ]

        self.border = False  # at the edge of the map
