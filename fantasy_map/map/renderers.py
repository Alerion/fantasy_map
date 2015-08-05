"""
For visual debugging.
"""
import matplotlib
import matplotlib.pyplot as plt


class MatplotRenderer(object):

    def __init__(self):
        plt.figure(figsize=(10, 10))
        plt.axis([-0.05, 1.05, -0.05, 1.05])
        self.ax = plt.subplot(1, 1, 1)

    def render_centers(self, map_obj):
        for center in map_obj.centers:
            p = matplotlib.patches.Polygon([c.point for c in center.corners], facecolor=(1, 1, 1))
            self.ax.add_patch(p)

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
        for corner in map_obj.corners:
            self.ax.plot([corner.point[0]], [corner.point[1]], '.')

        plt.show()

    def render_edges(self, map_obj):
        for edge in map_obj.edges:
            self.ax.plot(
                [edge.corners[0].point[0], edge.corners[1].point[0]],
                [edge.corners[0].point[1], edge.corners[1].point[1]],
                'k-')

            if len(edge.centers) == 2:
                self.ax.plot(
                    [edge.centers[0].point[0], edge.centers[1].point[0]],
                    [edge.centers[0].point[1], edge.centers[1].point[1]],
                    'k--')

        plt.show()
