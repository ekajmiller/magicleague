# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguematches', '0004_auto_20150426_0145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='season',
        ),
        migrations.AlterField(
            model_name='matchreport',
            name='round',
            field=models.PositiveIntegerField(choices=[(1, b'Round 1'), (2, b'Round 2'), (3, b'Round 3'), (4, b'Round 4'), (5, b'Round 5')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='seasons',
            field=models.ManyToManyField(to='leaguematches.Season', blank=True),
        ),
        migrations.DeleteModel(
            name='Round',
        ),
    ]
