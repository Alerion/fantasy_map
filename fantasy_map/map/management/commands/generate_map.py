"""
Inspired by http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/

Used:
    - https://stackoverflow.com/questions/20515554/colorize-voronoi-diagram/20678647#20678647
"""
from __future__ import division

from django.core.management.base import BaseCommand

from fantasy_map.map import (
    graph_generators, points_generators, renderers, land_generators, elevation_generators
)
from fantasy_map.map.map import Map


class Command(BaseCommand):
    help = 'Generate new map'

    def handle(self, *args, **options):
        map_obj = Map(1, [
            points_generators.RelaxedPoints(points_number=1000).generate_points,
            graph_generators.VoronoiGraph().generate_graph,
            # TODO: add this https://github.com/amitp/mapgen2/blob/master/Map.as#L215
            land_generators.SimplexIsland().generate_land,
            elevation_generators.FromCoast().generate_elevation,
            renderers.ElevationRenderer().render,
            # renderers.LandRendered().render
            # renderers.GraphRenderer().render_corners
        ])

        map_obj.generate()
