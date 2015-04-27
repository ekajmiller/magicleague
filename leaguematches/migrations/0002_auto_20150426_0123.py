# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguematches', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='email',
        ),
        migrations.RemoveField(
            model_name='player',
            name='fullname',
        ),
        migrations.RemoveField(
            model_name='player',
            name='shortname',
        ),
        migrations.AddField(
            model_name='player',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='password',
            field=models.CharField(default='', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
