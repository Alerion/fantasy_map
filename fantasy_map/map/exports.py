from __future__ import division

import cProfile
import math
import gdal
import numpy as np
import osr
import os
import pstats

from django.conf import settings
from django.contrib.gis.geos import Polygon, MultiPolygon
from scipy.ndimage.filters import gaussian_filter
from shapely.geometry import Polygon as Poly, Point

# 5624515 function calls in 9.509 seconds


def profile(func):
    """Decorator for run function profile"""
    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.prof'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        p = pstats.Stats(profile_filename)
        p.sort_stats('time').print_stats(10)
        return result
    return wrapper


class ModelExporter(object):

    def __init__(self, model, max_lat, max_lng):
        self.model = model
        self.max_lat = max_lat
        self.max_lng = max_lng

    def export(self, map_obj):
        self.model.objects.all().delete()
        new_objects = []

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
            new_objects.append(obj)

        self.model.objects.bulk_create(new_objects)

    def point_to_lnglat(self, point):
        return (
            self.max_lng * point[0] - self.max_lng / 2,
            self.max_lat * point[1] - self.max_lat / 2
        )


class GeoTiffExporter(object):

    def __init__(self, max_lat, max_lng):
        self.max_lat = max_lat
        self.max_lng = max_lng
        self.dst_filename = os.path.join(settings.BASE_DIR, 'map.tif')
        self.top_left_point = (-(max_lng / 2), max_lat / 2)
        self.bot_right_point = (max_lng / 2, -(max_lat / 2))
        self.max_height = 500  # elevation will be scaled to this value
        self.width = 1000

    # @profile
    def export(self, map_obj):
        # http://www.gdal.org/gdal_tutorial.html
        # http://blambi.blogspot.com/2010/05/making-geo-referenced-images-in-python.html
        in_srs = self.get_in_projection()
        out_srs = self.get_out_projection()
        coord_transform = osr.CoordinateTransformation(in_srs, out_srs)

        top_left_lng_m, top_left_lat_m, _ = coord_transform.TransformPoint(*self.top_left_point)
        bot_right_lng_m, bot_right_lat_m, _ = coord_transform.TransformPoint(*self.bot_right_point)

        # image size
        x_pixels = self.width
        PIXEL_SIZE = abs(top_left_lng_m - bot_right_lng_m) / x_pixels
        y_pixels = int(abs(bot_right_lat_m - top_left_lat_m) / PIXEL_SIZE) + 1
        x_pixels += 1

        # pixel/coords transform and inverse transform
        geo = [top_left_lng_m, PIXEL_SIZE, 0, top_left_lat_m, 0, -PIXEL_SIZE]
        inv_geo = gdal.InvGeoTransform(geo)[1]
        image_data = self.get_image_data(map_obj, (y_pixels, x_pixels), inv_geo, coord_transform)
        image_data = gaussian_filter(image_data, sigma=1)

        image_data *= self.max_height
        image_data = self.add_hillshade(image_data, 225, 45)

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
        dataset.FlushCache()

    def get_image_data(self, map_obj, size, inv_geo, coord_transform):
        cache_file_name = 'height_map_cache/%s_%s_%s.npy' % (map_obj.seed, len(map_obj.points), self.width)
        cache_file_path = os.path.join(settings.BASE_DIR, cache_file_name)

        try:
            return np.load(cache_file_path)
        except IOError:
            pass

        raster = np.zeros(size, dtype=np.float32)

        step = 0.5 / size[0]
        count = len(map_obj.centers)
        completed = 0
        for center in map_obj.centers:
            completed += 1
            if completed % 100 == 0:
                print '%s of %s' % (completed, count)

            if center.water:
                continue

            v1 = np.array([center.point[0], center.point[1], center.elevation])

            for edge in center.borders:
                c1 = edge.corners[0]
                c2 = edge.corners[1]
                cp1 = c1.point
                cp2 = c2.point

                # get the equation of a plane from three points
                v2 = np.array([cp1[0], cp1[1], c1.elevation])
                v3 = np.array([cp2[0], cp2[1], c2.elevation])
                normal = np.cross(v2 - v1, v3 - v1)
                a, b, c = normal
                d = np.dot(normal, v3)

                # calculate elevation for all points in polygon
                poly = Poly([center.point, cp1, cp2])
                minx, miny, maxx, maxy = poly.bounds

                for x in np.arange(minx, maxx, step):
                    for y in np.arange(miny, maxy, step):
                        if in_triange((x, y), v1, cp1, cp2):
                            # calculate elevation and convert to pixel value
                            z = (a * x + b * y - d) / -c
                            # get pixel coordinates from our coordinates(0-1)
                            img_x, img_y = self.point_to_pixel((x, y), inv_geo, coord_transform)
                            raster[img_y][img_x] = z

        np.save(cache_file_path, raster)
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

    def add_hillshade(self, array, azimuth, angle_altitude):
        """
        From here http://geoexamples.blogspot.com/2014/03/shaded-relief-images-using-gdal-python.html
        """
        x, y = np.gradient(array)
        slope = np.pi / 2. - np.arctan(np.sqrt(x * x + y * y))
        aspect = np.arctan2(-x, y)
        azimuthrad = azimuth * np.pi / 180.
        altituderad = angle_altitude*np.pi / 180.

        shaded = np.sin(altituderad) * np.sin(slope) + np.cos(altituderad) * np.cos(slope) \
            * np.cos(azimuthrad - aspect)
        return 255 * (shaded + 1) / 2


def in_triange(pt, v1, v2, v3):
    b1 = ((pt[0] - v2[0]) * (v1[1] - v2[1]) - (v1[0] - v2[0]) * (pt[1] - v2[1])) <= 0
    b2 = ((pt[0] - v3[0]) * (v2[1] - v3[1]) - (v2[0] - v3[0]) * (pt[1] - v3[1])) <= 0
    b3 = ((pt[0] - v1[0]) * (v3[1] - v1[1]) - (v3[0] - v1[0]) * (pt[1] - v1[1])) <= 0
    return (b1 == b2) and (b2 == b3)
