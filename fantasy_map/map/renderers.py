"""
For visual debugging.
"""
from __future__ import division

import gdal
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import osr
from django.contrib.gis.gdal import GDALRaster
from matplotlib.patches import Polygon
from noise import snoise2
from shapely.geometry import Polygon as Poly, Point


class MatplotRenderer(object):

    def __init__(self, verbose=False):
        self.verbose = verbose
        plt.figure(figsize=(12, 12))
        plt.axis([-0.05, 1.05, -0.05, 1.05])
        self.ax = plt.subplot(1, 1, 1)


class GraphRenderer(MatplotRenderer):

    def render_centers(self, map_obj):
        for center in map_obj.centers:
            facecolor = (1, 1, 1)
            if center.border:
                facecolor = (0.2, 0.2, 0.8)
            p = Polygon([c.point for c in center.corners], facecolor=facecolor)
            self.ax.add_patch(p)

            if self.verbose:
                for edge in center.borders:
                    self.ax.plot(
                        [center.point[0], edge.midpoint[0]],
                        [center.point[1], edge.midpoint[1]],
                        'k--')

                for neigh in center.neighbors:
                    self.ax.plot(
                        [center.point[0], neigh.point[0]],
                        [center.point[1], neigh.point[1]],
                        'k:')

        plt.show()

    def render_corners(self, map_obj):
        x = [corner.point[0] for corner in map_obj.corners if not corner.border]
        y = [corner.point[1] for corner in map_obj.corners if not corner.border]
        self.ax.plot(x, y, 'go')

        x = [corner.point[0] for corner in map_obj.corners if corner.border]
        y = [corner.point[1] for corner in map_obj.corners if corner.border]
        self.ax.plot(x, y, 'b.')

        for corner in map_obj.corners:
            for neigh in corner.adjacent:
                self.ax.plot(
                    [corner.point[0], neigh.point[0]],
                    [corner.point[1], neigh.point[1]],
                    'k:')

        plt.show()

    def render_edges(self, map_obj):
        for edge in map_obj.edges:
            style = 'k-'
            if edge.border:
                style = 'g--'
            self.ax.plot(
                [edge.corners[0].point[0], edge.corners[1].point[0]],
                [edge.corners[0].point[1], edge.corners[1].point[1]],
                style)

            if self.verbose:
                for center in edge.centers:
                    self.ax.plot(
                        [center.point[0], edge.midpoint[0]],
                        [center.point[1], edge.midpoint[1]],
                        'k--')

        plt.show()


class LandRendered(MatplotRenderer):

    def render(self, map_obj):
        for center in map_obj.centers:
            facecolor = '#ac9f8b'

            if center.water:
                facecolor = '#1b6ee3'

            if center.ocean:
                facecolor = '#abceff'

            if center.coast:
                facecolor = '#f0f5ea'

            p = Polygon([c.point for c in center.corners], facecolor=facecolor)
            self.ax.add_patch(p)

        # render water corners
        x = [corner.point[0] for corner in map_obj.corners if corner.water]
        y = [corner.point[1] for corner in map_obj.corners if corner.water]
        self.ax.plot(x, y, 'o', markerfacecolor='#1b6ee3')

        # render ocean corners
        x = [corner.point[0] for corner in map_obj.corners if corner.ocean]
        y = [corner.point[1] for corner in map_obj.corners if corner.ocean]
        self.ax.plot(x, y, 'o', markerfacecolor='#abceff')

        # render ocean corners
        x = [corner.point[0] for corner in map_obj.corners if corner.coast]
        y = [corner.point[1] for corner in map_obj.corners if corner.coast]
        self.ax.plot(x, y, 'o', markerfacecolor='#f0f5ea')

        plt.show()


class ElevationRenderer(MatplotRenderer):

    def __init__(self, verbose=False, rivers=True):
        self.rivers = rivers
        super(ElevationRenderer, self).__init__(verbose)

    def render(self, map_obj):
        for corner in map_obj.corners:
            if self.rivers and corner.river:
                markerfacecolor = '#1b6ee3'
            else:
                col = 1 - corner.elevation
                markerfacecolor = (col, col, col)
            self.ax.plot([corner.point[0]], [corner.point[1]], 'o', markerfacecolor=markerfacecolor)

        for center in map_obj.centers:
            if center.water:
                facecolor = '#1b6ee3'
                if center.ocean:
                    facecolor = '#abceff'
            else:
                col = 0.2 + (1 - center.elevation) * 0.8
                facecolor = (col, col, col)

            p = Polygon([c.point for c in center.corners], facecolor=facecolor)
            self.ax.add_patch(p)

        if self.rivers:
            for edge in map_obj.edges:
                if not edge.river:
                    continue

                self.ax.plot(
                    [edge.corners[0].point[0], edge.corners[1].point[0]],
                    [edge.corners[0].point[1], edge.corners[1].point[1]],
                    '-', color='#1b6ee3', linewidth=edge.river)

        plt.show()


class MoistureRenderer(MatplotRenderer):

    def render(self, map_obj):
        for corner in map_obj.corners:
            col = 1 - corner.moisture
            markerfacecolor = (col, col, col)
            self.ax.plot([corner.point[0]], [corner.point[1]], 'o', markerfacecolor=markerfacecolor)

        for center in map_obj.centers:
            if center.water:
                facecolor = '#1b6ee3'
                if center.ocean:
                    facecolor = '#abceff'
            else:
                col = 0.2 + (1 - center.elevation) * 0.8
                facecolor = (col, col, col)

            p = Polygon([c.point for c in center.corners], facecolor=facecolor)
            self.ax.add_patch(p)

        for edge in map_obj.edges:
            if not edge.river:
                continue

            self.ax.plot(
                [edge.corners[0].point[0], edge.corners[1].point[0]],
                [edge.corners[0].point[1], edge.corners[1].point[1]],
                '-', color='#1b6ee3', linewidth=edge.river)

        plt.show()


class BiomeRenderer(MatplotRenderer):

    def render(self, map_obj):
        light_vector = np.array([1, 1, 1])

        for center in map_obj.centers:
            biome_color = center.biome_color
            if center.water:
                p = Polygon([c.point for c in center.corners], color=biome_color)
                self.ax.add_patch(p)
            else:
                for edge in center.borders:
                    lightning = calc_lightning(center, edge, light_vector)
                    color_low = interpolate_color(biome_color, '#333333', 0.7)
                    color_high = interpolate_color(biome_color, '#ffffff', 0.3)
                    if lightning < 0.5:
                        color = interpolate_color(color_low, biome_color, lightning)
                    else:
                        color = interpolate_color(biome_color, color_high, lightning)

                    poly = [center.point, edge.corners[0].point, edge.corners[1].point]
                    self.ax.add_patch(Polygon(poly, color=color, linewidth=2, linestyle='dotted'))

        for edge in map_obj.edges:
            if not edge.river:
                continue

            self.ax.plot(
                [edge.corners[0].point[0], edge.corners[1].point[0]],
                [edge.corners[0].point[1], edge.corners[1].point[1]],
                '-', color='#1b6ee3', linewidth=edge.river)

        plt.show()


def calc_lightning(center, edge, light_vector):
    # Return light level for each edge (0-1).
    light_vector = light_vector / np.linalg.norm(light_vector)

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
    if normal[2] < 0:
        normal *= -1

    normal = normal / np.linalg.norm(normal)
    return 0.5 + 0.5 * np.dot(normal, light_vector)


def interpolate_color(color1, color2, f):
    """
    Helper function for color manipulation. When f==0: color1, f==1: color2
    """
    color1 = [int(color1[x:x+2], 16) for x in [1, 3, 5]]
    color2 = [int(color2[x:x+2], 16) for x in [1, 3, 5]]
    r = (1 - f) * color1[0] + f * color2[0]
    g = (1 - f) * color1[1] + f * color2[1]
    b = (1 - f) * color1[2] + f * color2[2]

    if r > 255:
        r = 0
    if g > 255:
        g = 0
    if b > 255:
        b = 0
    return '#%02x%02x%02x' % (r, g, b)


class GeoTiff(object):

    def render(self, map_obj):
        # http://www.gdal.org/gdal_tutorial.html
        # http://gis.stackexchange.com/questions/58517/python-gdal-save-array-as-raster-with-projection-from-other-file
        # http://gis.stackexchange.com/questions/62343/how-can-i-convert-a-ascii-file-to-geotiff-using-python
        dst_filename = '/home/alerion/Workspace/fantasy_map/map.tif'
        projection = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'
        x_pixels = 1000
        y_pixels = 1000
        PIXEL_SIZE = 600
        x_min = -(x_pixels / 2 * PIXEL_SIZE)
        y_max = y_pixels / 2 * PIXEL_SIZE
        driver = gdal.GetDriverByName('GTiff')

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(3857)

        dataset = driver.Create(
            dst_filename,
            x_pixels,
            y_pixels,
            1,
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

        ds1 = GDALRaster(dst_filename)
        ds2 = GDALRaster('/home/alerion/Workspace/fantasy_map/cea.tif')

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
                            raster[i][j] = int(65535 * (1 - z))
