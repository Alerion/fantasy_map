# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_biome'),
    ]

    operations = [
        migrations.CreateModel(
            name='River',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('width', models.PositiveIntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
            ],
        ),
        migrations.AlterField(
            model_name='biome',
            name='biome',
            field=models.CharField(choices=[('BARE', 'Bare'), ('BEACH', 'Beach'), ('GRASSLAND', 'Grassland'), ('ICE', 'Ice'), ('LAKE', 'Lake'), ('MARSH', 'Marsh'), ('OCEAN', 'OCEAN'), ('SCORCHED', 'Scorched'), ('SHRUBLAND', 'Shrubland'), ('SNOW', 'Snow'), ('SUBTROPICAL_DESERT', 'Subtropical deset'), ('TAIGA', 'Taiga'), ('TEMPERATE_DECIDUOUS_FOREST', 'Deciduous foreset'), ('TEMPERATE_DESERT', 'Desert'), ('TEMPERATE_RAIN_FOREST', 'Rain forest'), ('TROPICAL_RAIN_FOREST', 'Tropical rain forest'), ('TROPICAL_SEASONAL_FOREST', 'Tropical seasonal forest'), ('TUNDRA', 'Tundra')], max_length=50),
        ),
    ]
