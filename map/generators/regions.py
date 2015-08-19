import numpy as np
import random
from scipy.spatial import KDTree

from ..map import Region


def key(p1, p2=None):
    if p2 is None:
        return tuple(p1)
    return tuple(sorted([tuple(p1), tuple(p2)]))


class Cells:

    def __init__(self, cell_size=0.075):
        self.cell_size = cell_size

    def generate(self, map_obj):
        kdtree = KDTree([center.point for center in map_obj.centers])
        centers_index = {}

        for center in map_obj.centers:
            centers_index[key(center.point)] = center

        for x in np.arange(0, 1, self.cell_size):
            for y in np.arange(0, 1, self.cell_size):
                _, index = kdtree.query([x, y])
                point = kdtree.data[index]
                center = centers_index[key(point)]

                if center.water:
                    continue

                region = Region()
                region.centers.append(center)
                center.region = region
                map_obj.regions.append(region)

        while True:
            changed = False
            random.shuffle(map_obj.regions)
            for region in map_obj.regions:
                free_neighbors = region.free_neighbors
                if free_neighbors:
                    neighbor = random.choice(free_neighbors)
                    neighbor.region = region
                    region.centers.append(neighbor)
                    changed = True

            if not changed:
                break

        for center in map_obj.centers:
            if not center.region:
                center.region = Region()
                center.region.centers.append(center)
                map_obj.regions.append(region)
