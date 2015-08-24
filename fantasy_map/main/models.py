from django.contrib.gis.db import models

BIOMES = (
    ('BARE', 'Bare'),
    ('BEACH', 'Beach'),
    ('GRASSLAND', 'Grassland'),
    ('ICE', 'Ice'),
    ('LAKE', 'Lake'),
    ('MARSH', 'Marsh'),
    ('OCEAN', 'OCEAN'),
    ('SCORCHED', 'Scorched'),
    ('SHRUBLAND', 'Shrubland'),
    ('SNOW', 'Snow'),
    ('SUBTROPICAL_DESERT', 'Subtropical deset'),
    ('TAIGA', 'Taiga'),
    ('TEMPERATE_DECIDUOUS_FOREST', 'Deciduous foreset'),
    ('TEMPERATE_DESERT', 'Desert'),
    ('TEMPERATE_RAIN_FOREST', 'Rain forest'),
    ('TROPICAL_RAIN_FOREST', 'Tropical rain forest'),
    ('TROPICAL_SEASONAL_FOREST', 'Tropical seasonal forest'),
    ('TUNDRA', 'Tundra'),
)


class Biome(models.Model):
    biome = models.CharField(max_length=50, choices=BIOMES)
    border = models.BooleanField()
    coast = models.BooleanField()
    ocean = models.BooleanField()
    water = models.BooleanField()
    elevation = models.FloatField()
    moisture = models.FloatField()
    river = models.BooleanField()
    neighbors = models.ManyToManyField('self')
    center = models.PointField(srid=4326)
    geom = models.MultiPolygonField(srid=4326)
    region = models.ForeignKey('Region', blank=True, null=True)

    def __str__(self):
        return str(self.pk)


class River(models.Model):
    width = models.PositiveIntegerField()
    geom = models.MultiLineStringField()


class Region(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=100)
    neighbors = models.ManyToManyField('self')

    def __str__(self):
        return self.name


class City(models.Model):
    biome = models.ForeignKey(Biome)
    capital = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region)
    coords = models.PointField(srid=4326)

    def __str__(self):
        return self.name


class Country(models.Model):
    scalerank = models.IntegerField()
    labelrank = models.IntegerField()
    featurecla = models.CharField(max_length=50)
    sovereignt = models.CharField(max_length=32)
    sov_a3 = models.CharField(max_length=3)
    adm0_dif = models.FloatField()
    level = models.FloatField()
    type = models.CharField(max_length=17)
    admin = models.CharField(max_length=40)
    adm0_a3 = models.CharField(max_length=3)
    geou_dif = models.FloatField()
    geounit = models.CharField(max_length=40)
    gu_a3 = models.CharField(max_length=3)
    su_dif = models.FloatField()
    subunit = models.CharField(max_length=40)
    su_a3 = models.CharField(max_length=3)
    name = models.CharField(max_length=26)
    abbrev = models.CharField(max_length=13)
    postal = models.CharField(max_length=4)
    name_forma = models.CharField(max_length=53)
    terr_field = models.CharField(max_length=32)
    name_sort = models.CharField(max_length=43)
    map_color = models.FloatField()
    pop_est = models.FloatField()
    gdp_md_est = models.FloatField()
    fips_10_field = models.FloatField()
    iso_a2 = models.CharField(max_length=3)
    iso_a3 = models.CharField(max_length=3)
    iso_n3 = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


# Auto-generated `LayerMapping` dictionary for Country model
country_mapping = {
    'scalerank': 'ScaleRank',
    'labelrank': 'LabelRank',
    'featurecla': 'FeatureCla',
    'sovereignt': 'SOVEREIGNT',
    'sov_a3': 'SOV_A3',
    'adm0_dif': 'ADM0_DIF',
    'level': 'LEVEL',
    'type': 'TYPE',
    'admin': 'ADMIN',
    'adm0_a3': 'ADM0_A3',
    'geou_dif': 'GEOU_DIF',
    'geounit': 'GEOUNIT',
    'gu_a3': 'GU_A3',
    'su_dif': 'SU_DIF',
    'subunit': 'SUBUNIT',
    'su_a3': 'SU_A3',
    'name': 'NAME',
    'abbrev': 'ABBREV',
    'postal': 'POSTAL',
    'name_forma': 'NAME_FORMA',
    'terr_field': 'TERR_',
    'name_sort': 'NAME_SORT',
    'map_color': 'MAP_COLOR',
    'pop_est': 'POP_EST',
    'gdp_md_est': 'GDP_MD_EST',
    'fips_10_field': 'FIPS_10_',
    'iso_a2': 'ISO_A2',
    'iso_a3': 'ISO_A3',
    'iso_n3': 'ISO_N3',
    'geom': 'MULTIPOLYGON',
}
