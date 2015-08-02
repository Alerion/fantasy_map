import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import mapnik

stylesheet = os.path.abspath(os.path.join(settings.BASE_DIR, 'world_style.xml'))


class Command(BaseCommand):
    help = 'Generate tiles from Biome model'

    def handle(self, *args, **options):
        map_obj = mapnik.Map(1000, 1000)  # EPSG:4326
        mapnik.load_map(map_obj, stylesheet)
        map_obj.zoom_all()
        mapnik.render_to_file(map_obj, 'world.png', 'png')
