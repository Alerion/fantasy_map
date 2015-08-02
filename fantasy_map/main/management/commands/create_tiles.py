import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import mapnik

stylesheet = os.path.abspath(os.path.join(settings.BASE_DIR, 'world_style.xml'))


class Command(BaseCommand):
    help = 'Generate tiles from Biome model'

    def handle(self, *args, **options):
        if not options['biome'] and not options['country']:
            raise CommandError('Define --biome or --country')

        map_obj = mapnik.Map(2000, 1000)  # EPSG:4326
        # EPSG:3857
        # map_obj.srs = '+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +a=6378137 +b=6378137 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'
        # map_obj.background = mapnik.Color('steelblue')

        mapnik.load_map(map_obj, stylesheet)
        map_obj.zoom_all()
        mapnik.render_to_file(map_obj, 'world.png', 'png')
