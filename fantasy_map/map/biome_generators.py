from __future__ import division
# TODO: Add generator that considers lat/long (distance to North and South poles).


class Moisture(object):

    def generate(self, map_obj):
        # Calculate moisture. Freshwater sources spread moisture: rivers
        # and lakes (not oceans). Saltwater sources have moisture but do
        # not spread it (we set it at the end, after propagation).
        corners_queue = []
        for corner in map_obj.corners:
            if corner.water and not corner.ocean:
                corner.moisture = 1
                corners_queue.append(corner)
            elif corner.river > 0:
                corner.moisture = min(3, 0.2 * corner.river)
                corners_queue.append(corner)

        while corners_queue:
            corner = corners_queue.pop(0)
            for neighbour in corner.adjacent:
                new_moisture = corner.moisture * 0.9
                if (new_moisture > neighbour.moisture):
                    neighbour.moisture = new_moisture
                    corners_queue.append(neighbour)

        # ocean moisture
        for corner in map_obj.corners:
            if corner.ocean or corner.coast:
                corner.moisture = 1

        self._redistribute_moisture(map_obj.land_corners)

        # calculate moisture and biome for centers
        for center in map_obj.centers:
            center.moisture = sum([c.moisture for c in center.corners]) / len(center.corners)
            center.biome = self.get_biome(center)

    def _redistribute_moisture(self, corners):
        """
        Change the overall distribution of moisture to be evenly distributed.
        """
        corners.sort(key=lambda c: c.moisture)
        for i, corner in enumerate(corners):
            corner.moisture = i / (len(corners) - 1)

    def get_biome(self, center):
        """
        +-----------+-----------------------------------------------------------------------+
        | Elevation |                             Moisture Zone                             |
        |   Zone    +-----------+-----------+-----------+-----------+-----------+-----------+
        |           |  6 (wet)  |      5    |     4     |     3     |     2     |  1 (dry)  |
        +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
        |           |                                   |           |           |           |
        |  4 (high) |                SNOW               |   TUNDRA  |    BARE   |  SCORCHED |
        |           |                                   |           |           |           |
        +-----------+-----------------------+-----------+-----------+-----------+-----------+
        |           |                       |                       |                       |
        |     3     |         TAIGA         |       SHRUBLAND       |    TEMPERATE DESERT   |
        |           |                       |                       |                       |
        +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
        |           | TEMPERATE |       TEMPERATE       |                       | TEMPERATE |
        |     2     |   RAIN    |       DECIDUOUS       |       GRASSLAND       |  DESERT   |
        |           |  FOREST   |        FOREST         |                       |           |
        +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
        |           |      TROPICAL RAIN    |   TROPICAL SEASONAL   |           |SUBTROPICAL|
        |  1 (low)  |         FOREST        |         FOREST        | GRASSLAND |  DESERT   |
        |           |                       |                       |           |           |
        +-----------+-----------------------+-----------------------+-----------+-----------+
        """
        elevation = center.elevation
        moisture = center.moisture

        if center.ocean:
            biome = 'OCEAN'
        elif center.water:
            if elevation < 0.1:
                # FIXME: fix lake elevation at first, not it is set to 0
                # biome = 'MARSH'
                biome = 'LAKE'
            elif elevation > 0.8:
                biome = 'ICE'
            else:
                biome = 'LAKE'
        elif center.coast:
            biome = 'BEACH'
        elif elevation > 0.8:
            if moisture > 0.50:
                biome = 'SNOW'
            elif moisture > 0.33:
                biome = 'TUNDRA'
            elif moisture > 0.16:
                biome = 'BARE'
            else:
                biome = 'SCORCHED'
        elif elevation > 0.6:
            if moisture > 0.66:
                biome = 'TAIGA'
            elif moisture > 0.33:
                biome = 'SHRUBLAND'
            else:
                biome = 'TEMPERATE_DESERT'
        elif elevation > 0.3:
            if moisture > 0.83:
                biome = 'TEMPERATE_RAIN_FOREST'
            elif moisture > 0.50:
                biome = 'TEMPERATE_DECIDUOUS_FOREST'
            elif moisture > 0.16:
                biome = 'GRASSLAND'
            else:
                biome = 'TEMPERATE_DESERT'
        else:
            if moisture > 0.66:
                biome = 'TROPICAL_RAIN_FOREST'
            elif moisture > 0.33:
                biome = 'TROPICAL_SEASONAL_FOREST'
            elif moisture > 0.16:
                biome = 'GRASSLAND'
            else:
                biome = 'SUBTROPICAL_DESERT'

        return biome
