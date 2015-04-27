# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguematches', '0002_auto_20150426_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.EmailField(default='', unique=True, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='fullname',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
