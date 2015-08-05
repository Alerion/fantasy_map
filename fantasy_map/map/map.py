import numpy as np


class Map(object):

    def __init__(self, seed, generators):
        self.seed = seed
        self.generators = generators
        np.random.seed(seed)

        self.points = []  # used just for graph generator
        self.centers = []
        self.edges = []
        self.corners = []

    def generate(self):
        # Not sure this is the best pattern
        for generator in self.generators:
            generator(self)
