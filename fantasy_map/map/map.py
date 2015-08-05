class Map(object):

    def __init__(self, generators):
        self.generators = generators
        self.centers = []
        self.edges = []
        self.corners = []

    def generate(self):
        # Not sure this is the best pattern
        for generator in self.generators:
            generator(self)
