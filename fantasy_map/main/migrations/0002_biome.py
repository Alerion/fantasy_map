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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('biome', models.CharField(max_length=50)),
                ('water', models.BooleanField()),
                ('coast', models.BooleanField()),
                ('border', models.BooleanField()),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('elevation', models.FloatField()),
                ('moisture', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
    ]
