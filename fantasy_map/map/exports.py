from __future__ import division

import math
import gdal
import numpy as np
import osr

from django.contrib.gis.gdal import GDALRaster
from django.contrib.gis.geos import Polygon, MultiPolygon
from shapely.geometry import Polygon as Poly, Point


class ModelExporter(object):

    def __init__(self, model, max_lat, max_lng):
        self.model = model
        self.max_lat = max_lat
        self.max_lng = max_lng

    def export(self, map_obj):
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

    def point_to_lnglat(self, point):
        return (
            self.max_lng * point[0] - self.max_lng / 2,
            self.max_lat * point[1] - self.max_lat / 2
        )


class GeoTiffExporter(object):

    def __init__(self, max_lat, max_lng):
        self.max_lat = max_lat
        self.max_lng = max_lng
        # FIXME: allow any sizes
        assert max_lng == max_lat

    def export(self, map_obj):
        # http://www.gdal.org/gdal_tutorial.html
        # http://gis.stackexchange.com/questions/58517/python-gdal-save-array-as-raster-with-projection-from-other-file
        # http://gis.stackexchange.com/questions/62343/how-can-i-convert-a-ascii-file-to-geotiff-using-python
        dst_filename = '/home/alerion/Workspace/fantasy_map/map.tif'
        x_pixels, y_pixels = 1000, 1000
        PIXEL_SIZE = self.max_lat * 60 * 60 / x_pixels
        x_min = -(x_pixels / 2 * PIXEL_SIZE)
        y_max = y_pixels / 2 * PIXEL_SIZE
        driver = gdal.GetDriverByName('GTiff')

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(3857)

        dataset = driver.Create(
            dst_filename,
            x_pixels,
            y_pixels,
            1,  # bands count
            gdal.GDT_UInt16)

        dataset.SetGeoTransform((
            x_min,    # 0
            PIXEL_SIZE,  # 1
            0,                      # 2
            y_max,    # 3
            0,                      # 4
            -PIXEL_SIZE))

        raster = np.zeros((x_pixels, y_pixels), dtype=np.uint16)
        raster.fill(65535)
        self._render_centers(map_obj, raster)

        dataset.SetProjection(srs.ExportToWkt())
        dataset.GetRasterBand(1).WriteArray(raster)
        dataset.FlushCache()  # Write to disk.

    def _render_centers(self, map_obj, raster):
        x_pixels = raster.shape[0]
        y_pixels = raster.shape[1]
        count = len(map_obj.centers)
        completed = 0
        for center in map_obj.centers:
            completed += 1
            if completed % 10 == 0:
                print '%s of %s' % (completed, count)

            if center.water:
                continue

            for edge in center.borders:
                c1 = edge.corners[0]
                c2 = edge.corners[1]

                v1 = np.array([
                    center.point[0],
                    center.point[1],
                    center.elevation
                ])

                v2 = np.array([
                    c1.point[0],
                    c1.point[1],
                    c1.elevation
                ])

                v3 = np.array([
                    c2.point[0],
                    c2.point[1],
                    c2.elevation
                ])

                normal = np.cross(v2 - v1, v3 - v1)
                a, b, c = normal
                d = np.dot(normal, v3)

                poly = Poly([center.point, c1.point, c2.point])
                minx, miny, maxx, maxy = poly.bounds
                minx = int(minx * x_pixels) - 1
                miny = int(miny * y_pixels) - 1
                maxx = int(maxx * x_pixels) + 1
                maxy = int(maxy * y_pixels) + 1

                for j in xrange(miny, maxy):
                    for i in xrange(minx, maxx):
                        x = i / x_pixels
                        y = j / y_pixels
                        if poly.contains(Point(x, y)):
                            z = (a * x + b * y - d) / -c
                            raster[j][i] = int(65535 * (1 - z))
