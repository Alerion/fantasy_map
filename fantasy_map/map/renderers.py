"""
For visual debugging.
"""
import matplotlib
import matplotlib.pyplot as plt


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
            p = matplotlib.patches.Polygon([c.point for c in center.corners], facecolor=facecolor)
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

            p = matplotlib.patches.Polygon([c.point for c in center.corners], facecolor=facecolor)
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
