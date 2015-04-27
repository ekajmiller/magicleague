# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguematches', '0005_auto_20150426_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchreport',
            name='season',
            field=models.ForeignKey(default=1, to='leaguematches.Season'),
            preserve_default=False,
        ),
    ]
