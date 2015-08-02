# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scalerank', models.IntegerField()),
                ('labelrank', models.IntegerField()),
                ('featurecla', models.CharField(max_length=50)),
                ('sovereignt', models.CharField(max_length=32)),
                ('sov_a3', models.CharField(max_length=3)),
                ('adm0_dif', models.FloatField()),
                ('level', models.FloatField()),
                ('type', models.CharField(max_length=17)),
                ('admin', models.CharField(max_length=40)),
                ('adm0_a3', models.CharField(max_length=3)),
                ('geou_dif', models.FloatField()),
                ('geounit', models.CharField(max_length=40)),
                ('gu_a3', models.CharField(max_length=3)),
                ('su_dif', models.FloatField()),
                ('subunit', models.CharField(max_length=40)),
                ('su_a3', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=26)),
                ('abbrev', models.CharField(max_length=13)),
                ('postal', models.CharField(max_length=4)),
                ('name_forma', models.CharField(max_length=53)),
                ('terr_field', models.CharField(max_length=32)),
                ('name_sort', models.CharField(max_length=43)),
                ('map_color', models.FloatField()),
                ('pop_est', models.FloatField()),
                ('gdp_md_est', models.FloatField()),
                ('fips_10_field', models.FloatField()),
                ('iso_a2', models.CharField(max_length=3)),
                ('iso_a3', models.CharField(max_length=3)),
                ('iso_n3', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
    ]
