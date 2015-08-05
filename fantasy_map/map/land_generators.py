from __future__ import division

from noise import pnoise2, snoise2
from pprint import pprint

LAKE_THRESHOLD = 0.35  # 0 to 1, fraction of water corners for water polygon


class PerlinIsland(object):
    """
    Generate lands with Perlin noise.
    """

    def __init__(self, octaves=8):
        self.octaves = octaves

    def generate_land(self, map_obj):
        # assign water for corners according to Perlin noise
        for corner in map_obj.corners:
            if corner.border:
                corner.water = True
                corner.ocean = True
            else:
                p = corner.point
                # TODO: play around with this parameters, try snoise2
                # now there is no lakes
                corner.water = pnoise2(p[0], p[1], self.octaves) >= 0

        ocean_polys = []
        for center in map_obj.centers:
            if center.border:
                center.water = True
                center.ocean = True
                ocean_polys.append(center)
            else:
                water_count = 0
                for corner in center.corners:
                    if corner.water:
                        water_count += 1
                center.water = water_count >= LAKE_THRESHOLD * len(center.corners)

        # fill center.ocean
        while ocean_polys:
            center = ocean_polys.pop()
            for neighbor in center.neighbors:
                if neighbor.water and not neighbor.ocean:
                    neighbor.ocean = True
                    ocean_polys.append(neighbor)

        # fill center.coast
        for center in map_obj.centers:
            if not center.water:
                center.coast = any(neigh.ocean for neigh in center.neighbors)
            else:
                # fix corner.water
                for corner in center.corners:
                    corner.water = True

        # fill corner.coast and corner.ocean
        for corner in map_obj.corners:
            if corner.water:
                corner.ocean = all(neigh.ocean for neigh in corner.touches)
                corner.coast = not corner.ocean
