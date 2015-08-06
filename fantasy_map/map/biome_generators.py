from __future__ import division


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

        # calculate moisture for centers
        for center in map_obj.centers:
            center.moisture = sum([c.moisture for c in center.corners]) / len(center.corners)

    def _redistribute_moisture(self, corners):
        """
        Change the overall distribution of moisture to be evenly distributed.
        """
        corners.sort(key=lambda c: c.moisture)
        for i, corner in enumerate(corners):
            corner.moisture = i / (len(corners) - 1)
