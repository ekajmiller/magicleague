# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguematches', '0003_auto_20150426_0140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='fullname',
        ),
        migrations.AddField(
            model_name='player',
            name='first_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='last_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
