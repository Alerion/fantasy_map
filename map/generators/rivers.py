import random


class RandomRiver:

    def __init__(self, points_part=0.1):
        self.points_part = points_part

    def generate(self, map_obj):
        random.seed(map_obj.seed)
        # calculate Corner.downslope and Corner.downslope_edge
        for corner in map_obj.corners:
            downslope = corner
            for neighbour in corner.adjacent:
                if neighbour.elevation <= downslope.elevation:
                    downslope = neighbour
            corner.downslope = downslope

            for edge in corner.protrudes:
                if downslope in edge.corners:
                    corner.downslope_edge = edge
                    break

        # TODO: calculate watersheds https://github.com/amitp/mapgen2/blob/master/Map.as#L605
        # Do we really need this?

        # generate rivers
        points = int(self.points_part * len(map_obj.points))
        for _ in range(points):
            corner = random.choice(map_obj.corners)

            if corner.ocean or corner.river or corner.elevation < 0.3 or corner.elevation > 0.9 \
                    or corner.downslope == corner:
                continue

            # move river to ocean or lake
            while not corner.water:
                corner.river += 1
                corner.downslope_edge.river += 1
                corner = corner.downslope
            # fix river value of estuary
            corner.river += 1
