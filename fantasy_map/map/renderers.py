"""
For visual debugging.
"""
from __future__ import division

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


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
        for center in map_obj.centers:
            biome_color = center.biome_color
            if center.water:
                p = Polygon([c.point for c in center.corners], color=biome_color)
                self.ax.add_patch(p)
            else:
                lightning = center.lightnings()
                for i, edge in enumerate(center.borders):
                    color_low = interpolate_color(biome_color, '#333333', 0.7)
                    color_high = interpolate_color(biome_color, '#ffffff', 0.3)
                    if lightning[i] < 0.5:
                        color = interpolate_color(color_low, biome_color, lightning[i])
                    else:
                        color = interpolate_color(biome_color, color_high, lightning[i])

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


class LightRender(MatplotRenderer):

    def render(self, map_obj):
        for center in map_obj.centers:
            if center.water:
                facecolor = '#1b6ee3'
                if center.ocean:
                    facecolor = '#abceff'
                p = Polygon([c.point for c in center.corners], facecolor=facecolor)
                self.ax.add_patch(p)
            else:
                lightning = center.lightnings()
                for i, edge in enumerate(center.borders):
                    col = lightning[i]
                    facecolor = (col, col, col)
                    poly = [center.point, edge.corners[0].point, edge.corners[1].point]
                    self.ax.add_patch(Polygon(poly, facecolor=facecolor))
        plt.show()
