import math
import os
from lxml import etree
from pprint import pprint

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Polygon, MultiPolygon

from fantasy_map.main.models import Biome

world_xml = os.path.abspath(os.path.join(settings.BASE_DIR, 'map/map.xml'))


class Command(BaseCommand):

    def handle(self, *args, **options):
        Biome.objects.all().delete()

        centers = {}
        edges = {}
        corners = {}

        with open(world_xml) as map_file:
            tree = etree.parse(map_file)

            center_nodes = tree.xpath('/map/centers/center')
            for node in center_nodes:
                if node.get('ocean') == 'false':
                    centers[node.get('id')] = node

            edge_nodes = tree.xpath('/map/edges/edge')
            for node in edge_nodes:
                edges[node.get('id')] = node

            corner_nodes = tree.xpath('/map/corners/corner')
            for node in corner_nodes:
                corners[node.get('id')] = node

        # FIXME: add smarter conversion
        max_x = max([float(node.get('x')) for node in centers.values()])
        max_y = max([float(node.get('y')) for node in centers.values()])
        max_lat = 50.
        max_lng = 50.

        for node in centers.values():
            obj = Biome(biome=node.get('biome'))
            obj.water = (node.get('water') == 'true')
            obj.coast = (node.get('coast') == 'true')
            obj.border = (node.get('border') == 'true')
            obj.elevation = float(node.get('elevation'))
            obj.moisture = float(node.get('moisture'))
            obj.lat = float(node.get('y')) * max_lat / max_y
            obj.lng = float(node.get('x')) * max_lng / max_x
            coords = []
            for cnode in node.xpath('corner'):
                corner = corners[cnode.get('id')]
                lat = float(corner.get('y')) * max_lat / max_y
                lng = float(corner.get('x')) * max_lng / max_x
                coords.append((lng, lat))
            # sort coordinates
            coords.sort(key=lambda p: math.atan2(p[1] - obj.lat, p[0] - obj.lng))
            coords.append(coords[0])

            obj.geom = MultiPolygon([Polygon(coords)])
            obj.full_clean()
            obj.save()
