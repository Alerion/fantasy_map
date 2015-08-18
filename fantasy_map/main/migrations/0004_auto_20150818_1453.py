# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150817_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='biome',
            name='neighbors',
            field=models.ManyToManyField(related_name='neighbors_rel_+', to='main.Biome'),
        ),
        migrations.AddField(
            model_name='biome',
            name='river',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
