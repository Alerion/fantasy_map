"""
Inspired by http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/

Used:
    - https://stackoverflow.com/questions/20515554/colorize-voronoi-diagram/20678647#20678647
"""
from __future__ import division

from django.core.management.base import BaseCommand

from fantasy_map.map.map import Map
from fantasy_map.map.graph_generators import VoronoiGenerator
from fantasy_map.map.renderers import MatplotRenderer


class Command(BaseCommand):
    help = 'Generate new map'

    def handle(self, *args, **options):
        map_obj = Map([
            VoronoiGenerator(points_number=50),
            MatplotRenderer().render_centers
        ])

        map_obj.generate()
