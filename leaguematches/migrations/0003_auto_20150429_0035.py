# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguematches', '0002_auto_20150427_0212'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('match', models.ForeignKey(to='leaguematches.MatchReport')),
                ('player', models.ForeignKey(to='leaguematches.Player')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='matchorder',
            unique_together=set([('player', 'match')]),
        ),
    ]
