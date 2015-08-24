# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150819_1545'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([]),
        ),
    ]
