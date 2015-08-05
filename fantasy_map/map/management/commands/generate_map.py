"""
Inspired by http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/

Used:
    - https://stackoverflow.com/questions/20515554/colorize-voronoi-diagram/20678647#20678647
"""
from __future__ import division

from django.core.management.base import BaseCommand

from fantasy_map.map import graph_generators
from fantasy_map.map import points_generators
from fantasy_map.map import renderers
from fantasy_map.map.map import Map


class Command(BaseCommand):
    help = 'Generate new map'

    def handle(self, *args, **options):
        map_obj = Map(100500, [
            points_generators.RelaxedPoints(points_number=100),
            graph_generators.VoronoiGraph(),
            renderers.MatplotRenderer().render_centers,
        ])

        map_obj.generate()
