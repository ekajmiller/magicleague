# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguematches', '0002_auto_20150517_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='calcmethod',
            field=models.CharField(default=b'Simple', max_length=30, choices=[(b'NegTieBreakLosses', b'Negative Tie Breaker Points for Losses'), (b'Simple', b"Regular scoring where order of matches doesn't matter for tiebreakers")]),
        ),
        migrations.AddField(
            model_name='season',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='season',
            name='current_round',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
