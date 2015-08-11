from __future__ import division

import math
import gdal
import numpy as np
import osr

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
        self.dst_filename = '/home/alerion/Workspace/fantasy_map/map.tif'
        self.top_left_point = (-(max_lng / 2), max_lat / 2)
        self.bot_right_point = (max_lng / 2, -(max_lat / 2))

    def export(self, map_obj):
        # http://www.gdal.org/gdal_tutorial.html
        # http://blambi.blogspot.com/2010/05/making-geo-referenced-images-in-python.html
        in_srs = self.get_in_projection()
        out_srs = self.get_out_projection()
        coord_transform = osr.CoordinateTransformation(in_srs, out_srs)

        top_left_lng_m, top_left_lat_m, _ = coord_transform.TransformPoint(*self.top_left_point)
        bot_right_lng_m, bot_right_lat_m, _ = coord_transform.TransformPoint(*self.bot_right_point)

        # image size
        x_pixels = 1000
        PIXEL_SIZE = abs(top_left_lng_m - bot_right_lng_m) / x_pixels
        y_pixels = int(abs(bot_right_lat_m - top_left_lat_m) / PIXEL_SIZE) + 1
        x_pixels += 1

        # pixel/coords transform and inverse transform
        geo = [top_left_lng_m, PIXEL_SIZE, 0, top_left_lat_m, 0, -PIXEL_SIZE]
        inv_geo = gdal.InvGeoTransform(geo)[1]
        image_data = self.get_image_data(map_obj, (y_pixels, x_pixels), inv_geo, coord_transform)

        # create image
        dataset = gdal.GetDriverByName('GTiff').Create(
            self.dst_filename,
            x_pixels,
            y_pixels,
            1,  # bands count
            gdal.GDT_Byte)

        dataset.SetGeoTransform(geo)
        dataset.SetProjection(out_srs.ExportToWkt())
        dataset.GetRasterBand(1).WriteArray(image_data)
        dataset.FlushCache()  # Write to disk.

    def get_image_data(self, map_obj, size, inv_geo, coord_transform):
        raster = np.zeros(size, dtype=np.uint8)
        raster.fill(255)

        count = len(map_obj.centers)
        completed = 0
        for center in map_obj.centers:
            completed += 1
            if completed % 100 == 0:
                print '%s of %s' % (completed, count)

            if center.water:
                continue

            for edge in center.borders:
                c1 = edge.corners[0]
                c2 = edge.corners[1]

                # get the equation of a plane from three points
                v1 = np.array([center.point[0], center.point[1], center.elevation])
                v2 = np.array([c1.point[0], c1.point[1], c1.elevation])
                v3 = np.array([c2.point[0], c2.point[1], c2.elevation])
                normal = np.cross(v2 - v1, v3 - v1)
                a, b, c = normal
                d = np.dot(normal, v3)

                # calculate elevation for all points in polygon
                poly = Poly([center.point, c1.point, c2.point])
                minx, miny, maxx, maxy = poly.bounds

                img_minx = int(minx * size[1]) - 1
                img_miny = int(miny * size[0]) - 1
                img_maxx = int(maxx * size[1]) + 1
                img_maxy = int(maxy * size[0]) + 1

                for j in xrange(img_miny, img_maxy):
                    for i in xrange(img_minx, img_maxx):
                        # convert image coordinates to our coordinates in range 0-1
                        x, y = (i / size[1]), (j / size[0])
                        if poly.contains(Point(x, y)):
                            # calculate elevation and convert to pixel value
                            z = (a * x + b * y - d) / -c
                            value = int(255 * (1 - z))
                            # get pixel coordinates from our coordinates(0-1)
                            img_x, img_y = self.point_to_pixel((x, y), inv_geo, coord_transform)
                            raster[img_y][img_x] = value

        for corner in map_obj.corners:
            x, y = self.point_to_pixel(corner.point, inv_geo, coord_transform)
            raster[y][x] = 0

        self.fix_raster(raster)
        return raster

    def get_in_projection(self):
        """
        We save our polygons in this projection.
        """
        proj = osr.SpatialReference()
        proj.ImportFromEPSG(4326)
        return proj

    def get_out_projection(self):
        """
        Output projection is projection of our map tiles.
        """
        proj = osr.SpatialReference()
        proj.ImportFromEPSG(3857)
        return proj

    def get_pixel(self, lng, lat, inv_geo, transform):
        """
        Return pixel coordinates from lng/lat
        """
        gx, gy, _ = transform.TransformPoint(lng, lat)
        gx, gy = gdal.ApplyGeoTransform(inv_geo, gx, gy)
        return int(gx), int(gy)

    def point_to_lnglat(self, point):
        """
        Convert point in our coordinates(0-1) to lng/lat
        """
        return (
            self.max_lng * point[0] - self.max_lng / 2,
            self.max_lat * point[1] - self.max_lat / 2
        )

    def point_to_pixel(self, point, inv_geo, transform):
        """
        Convert point in our coordinates(0-1) to pixel coordinates
        """
        lng, lat = self.point_to_lnglat(point)
        return self.get_pixel(lng, lat, inv_geo, transform)

    def fix_raster(self, raster):
        """
        Fix artifacts.
        """
        print(raster.shape)