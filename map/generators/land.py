from __future__ import division

from noise import snoise2

# TODO: add generator with Perlin noise, noise.pnoise2
LAKE_THRESHOLD = 0.35  # 0 to 1, fraction of water corners for water polygon


class SimplexIsland:
    """
    Generate lands with Simplex noise.
    """

    def __init__(self, islands_level=1.5, octaves=8, land_threshold=0):
        self.octaves = octaves
        self.land_threshold = land_threshold
        self.islands_level = islands_level

    def generate(self, map_obj):
        # assign water for corners according to Perlin noise
        for corner in map_obj.corners:
            if corner.border:
                corner.water = True
                corner.ocean = True
            else:
                p = corner.point
                val = snoise2(p[0] * self.islands_level, p[1] * self.islands_level,
                              self.octaves, base=map_obj.seed)
                corner.water = val < self.land_threshold

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
                corner.ocean = any(neigh.ocean for neigh in corner.touches)

                if corner.ocean:
                    corner.coast = any(not neigh.water for neigh in corner.touches)

                # fix noise "artifacts"
                if all(not neigh.water for neigh in corner.touches):
                    corner.water = False
