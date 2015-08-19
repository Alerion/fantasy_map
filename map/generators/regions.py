import numpy as np
import math
import random
from scipy.spatial import KDTree

from ..map import Region


def key(p1, p2=None):
    if p2 is None:
        return tuple(p1)
    return tuple(sorted([tuple(p1), tuple(p2)]))


class Grid:

    def __init__(self, cell_size=0.075):
        self.cell_size = cell_size

    def generate_capitals(self, map_obj):
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

                # Do not put capitals close on to other
                if any([neighbor.region for neighbor in center.neighbors]):
                    continue

                center.region = Region(center)
                map_obj.regions.append(center.region)

    def generate(self, map_obj):
        self.generate_capitals(map_obj)

        # Spread regions
        while True:
            changed = False
            random.shuffle(map_obj.regions)
            for region in map_obj.regions:
                free_neighbors = region.free_neighbors

                if free_neighbors:
                    neighbors = list(free_neighbors.keys())
                    probs = np.array(list(free_neighbors.values()))
                    probs /= probs.sum()

                    neighbor = np.random.choice(neighbors, p=probs)
                    region.add_center(neighbor)
                    changed = True

            if not changed:
                break

        # Create regions on small islands
        for center in map_obj.centers:
            if center.water or center.region:
                continue

            center.region = Region(center)
            map_obj.regions.append(center.region)

            free_neighbors = center.region.free_neighbors
            while free_neighbors:
                for neighbor in free_neighbors.keys():
                    center.region.add_center(neighbor)
                free_neighbors = center.region.free_neighbors


class HexGrid(Grid):

    def generate_capitals(self, map_obj):
        kdtree = KDTree([center.point for center in map_obj.centers])
        centers_index = {}

        for center in map_obj.centers:
            centers_index[key(center.point)] = center

        height = self.cell_size
        width = math.sqrt(3) / 2 * height
        row = 0
        x = height / 2

        while x < 1:
            if row % 2 == 0:
                y = width
            else:
                y = width / 2

            while y < 1:
                _, index = kdtree.query([x, y])
                point = kdtree.data[index]
                center = centers_index[key(point)]

                # Do not put capitals close on to other
                is_neighbor_capital = any([neighbor.region for neighbor in center.neighbors])

                if not center.water and not is_neighbor_capital:
                    center.region = Region(center)
                    map_obj.regions.append(center.region)

                y += width

            row += 1
            x += (height * 3 / 4)
