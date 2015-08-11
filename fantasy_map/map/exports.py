from __future__ import division

import math
from django.contrib.gis.geos import Polygon, MultiPolygon


class ModelExporter(object):

    def __init__(self, model, max_lat, max_lng):
        self.model = model
        self.max_lat = max_lat
        self.max_lng = max_lng

    def export(self, map_obj):
        print('Delete %s objects' % self.model.objects.count())
        self.model.objects.all().delete()
        for center in map_obj.centers:
            # Do not save ocean for optimization
            # FIXME: But we need them
            if center.ocean:
                continue

            obj = self.model()
            obj.biome = center.biome
            obj.water = center.water
            obj.coast = center.coast
            obj.border = center.border
            obj.elevation = center.elevation
            obj.moisture = center.moisture
            obj.lng, obj.lat = self.point_to_lnglat(center.point)

            coords = []
            for corner in center.corners:
                coords.append(self.point_to_lnglat(corner.point))
            # Sort coordinates. Should be sorted already, but lets check once more.
            coords.sort(key=lambda p: math.atan2(p[1] - obj.lat, p[0] - obj.lng))
            coords.append(coords[0])

            obj.geom = MultiPolygon([Polygon(coords)])
            obj.full_clean()
            obj.save()
        print(self.model.objects.count())

    def point_to_lnglat(self, point):
        return (
            self.max_lng * point[0] - self.max_lng / 2,
            self.max_lat * point[1] - self.max_lat / 2
        )
