# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguematches', '0001_squashed_0006_matchreport_season'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matchreport',
            options={'ordering': ['round', 'played_date', 'report_date']},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['first_name', 'last_name']},
        ),
        migrations.AlterUniqueTogether(
            name='matchreport',
            unique_together=set([('played_date', 'reporter', 'opponent')]),
        ),
    ]
