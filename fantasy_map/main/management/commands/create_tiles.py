from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import mapnik
from fantasy_map.main.models import Country, Biome

BIOMES = (
    ('TEMPERATE_RAIN_FOREST', '#a4c4a8'),
    ('TEMPERATE_DESERT', '#e4e8ca'),
    ('SNOW', '#f8f8f8'),
    ('SUBTROPICAL_DESERT', '#e9ddc7'),
    ('TEMPERATE_DECIDUOUS_FOREST', '#b4c9a9'),
    ('TAIGA', '#ccd4bb'),
    ('TROPICAL_RAIN_FOREST', '#9cbba9'),
    ('LAKE', '#2464ab'),
    ('BARE', '#bbbbbb'),
    ('TUNDRA', '#999999'),
    ('GRASSLAND', '#c4d4aa'),
    ('TROPICAL_SEASONAL_FOREST', '#a9cca4'),
    ('SHRUBLAND', '#c4ccbb'),
    ('BEACH', '#ac9f8b'),
)


class Command(BaseCommand):
    help = 'Generate tiles from Country'

    def add_arguments(self, parser):
        parser.add_argument(
            '--biome',
            action='store_true',
            dest='biome',
            default=False,
            help='Create tiles for Biome')

        parser.add_argument(
            '--country',
            action='store_true',
            dest='country',
            default=False,
            help='Create tiles for Country')

    def handle(self, *args, **options):
        if not options['biome'] and not options['country']:
            raise CommandError('Define --biome or --country')

        model = None
        if options['biome']:
            model = Biome
        elif options['country']:
            model = Country

        map_obj = mapnik.Map(2000, 1000)
        map_obj.background = mapnik.Color('steelblue')
        style = mapnik.Style()

        for biome, color in BIOMES:
            rule = mapnik.Rule()
            polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color(color))
            rule.symbols.append(polygon_symbolizer)
            rule.symbols.append(mapnik.LineSymbolizer(mapnik.Color(color), 1))
            rule.filter = mapnik.Filter("[biome] = '%s'" % biome)
            style.rules.append(rule)

        map_obj.append_style('My Style', style)

        db_settings = settings.DATABASES['default']
        layer = mapnik.Layer('world')
        layer.datasource = mapnik.PostGIS(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            dbname=db_settings['NAME'],
            table=model._meta.db_table)
        layer.styles.append('My Style')

        map_obj.layers.append(layer)
        map_obj.zoom_all()
        mapnik.render_to_file(map_obj, 'world.png', 'png')
