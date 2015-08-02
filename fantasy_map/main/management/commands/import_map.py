import os

from django.contrib.gis.utils import LayerMapping
from django.core.management.base import BaseCommand
from django.conf import settings

from fantasy_map.main.models import Country, country_mapping


world_shp = os.path.abspath(os.path.join(settings.BASE_DIR, 'map/ne_110m_admin_0_countries.shp'))


class Command(BaseCommand):
    help = 'Import counties to DB'

    def handle(self, *args, **options):
        lm = LayerMapping(Country, world_shp, country_mapping,
                          transform=False, encoding='iso-8859-1')

        lm.save(strict=True, verbose=True)
