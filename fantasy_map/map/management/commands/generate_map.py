"""
Inspired by http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/

Used:
    - https://stackoverflow.com/questions/20515554/colorize-voronoi-diagram/20678647#20678647
"""
from __future__ import division

import random

from django.core.management.base import BaseCommand

from fantasy_map.map import (
    graph_generators, points_generators, renderers, land_generators, elevation_generators,
    river_generators, biome_generators, exports
)
from fantasy_map.map.map import Map
from fantasy_map.main.models import Biome


class Command(BaseCommand):
    help = 'Generate new map'

    def add_arguments(self, parser):
        parser.add_argument('--seed', action="store", dest="seed", type=int)

    def handle(self, seed=None, *args, **options):
        if seed is None:
            seed = int(random.random() * 10000)
        print('seed = %s' % seed)
        map_obj = Map(seed, [
            points_generators.RelaxedPoints(points_number=1000).generate,
            graph_generators.VoronoiGraph().generate,
            # TODO: add this https://github.com/amitp/mapgen2/blob/master/Map.as#L215
            land_generators.SimplexIsland().generate,
            elevation_generators.FromCoast().generate,
            river_generators.RandomRiver().generate,
            biome_generators.Moisture().generate,
            exports.ModelExporter(Biome, max_lat=70., max_lng=70.).export,
            # renderers.GeoTiff().render,
            # renderers.BiomeRenderer().render,
        ])

        map_obj.generate()
