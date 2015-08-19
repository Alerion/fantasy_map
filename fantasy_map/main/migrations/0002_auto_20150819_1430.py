# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Biome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('biome', models.CharField(choices=[('BARE', 'Bare'), ('BEACH', 'Beach'), ('GRASSLAND', 'Grassland'), ('ICE', 'Ice'), ('LAKE', 'Lake'), ('MARSH', 'Marsh'), ('OCEAN', 'OCEAN'), ('SCORCHED', 'Scorched'), ('SHRUBLAND', 'Shrubland'), ('SNOW', 'Snow'), ('SUBTROPICAL_DESERT', 'Subtropical deset'), ('TAIGA', 'Taiga'), ('TEMPERATE_DECIDUOUS_FOREST', 'Deciduous foreset'), ('TEMPERATE_DESERT', 'Desert'), ('TEMPERATE_RAIN_FOREST', 'Rain forest'), ('TROPICAL_RAIN_FOREST', 'Tropical rain forest'), ('TROPICAL_SEASONAL_FOREST', 'Tropical seasonal forest'), ('TUNDRA', 'Tundra')], max_length=50)),
                ('water', models.BooleanField()),
                ('coast', models.BooleanField()),
                ('border', models.BooleanField()),
                ('elevation', models.FloatField()),
                ('moisture', models.FloatField()),
                ('river', models.BooleanField()),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('neighbors', models.ManyToManyField(related_name='neighbors_rel_+', to='main.Biome')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('capital', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('coords', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('biome', models.ForeignKey(to='main.Biome')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('name', models.CharField(max_length=100)),
                ('neighbors', models.ManyToManyField(related_name='neighbors_rel_+', to='main.Region')),
            ],
        ),
        migrations.CreateModel(
            name='River',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('width', models.PositiveIntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(to='main.Region'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('region', 'capital')]),
        ),
    ]
