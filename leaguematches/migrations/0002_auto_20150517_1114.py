# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leaguematches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MatchReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round', models.PositiveIntegerField(choices=[(1, b'Round 1'), (2, b'Round 2'), (3, b'Round 3'), (4, b'Round 4'), (5, b'Round 5')])),
                ('report_date', models.DateTimeField()),
                ('played_date', models.DateField()),
                ('win', models.BooleanField(choices=[(True, b'Win'), (False, b'Loss')])),
                ('verified', models.BooleanField()),
            ],
            options={
                'ordering': ['round', 'played_date', 'report_date'],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='seasons',
            field=models.ManyToManyField(to='leaguematches.Season', blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='matchreport',
            name='loser',
            field=models.ForeignKey(related_name='+', to='leaguematches.Player'),
        ),
        migrations.AddField(
            model_name='matchreport',
            name='opponent',
            field=models.ForeignKey(related_name='+', to='leaguematches.Player'),
        ),
        migrations.AddField(
            model_name='matchreport',
            name='reporter',
            field=models.ForeignKey(related_name='+', to='leaguematches.Player'),
        ),
        migrations.AddField(
            model_name='matchreport',
            name='season',
            field=models.ForeignKey(to='leaguematches.Season'),
        ),
        migrations.AddField(
            model_name='matchreport',
            name='winner',
            field=models.ForeignKey(related_name='+', to='leaguematches.Player'),
        ),
        migrations.AddField(
            model_name='matchorder',
            name='match',
            field=models.ForeignKey(to='leaguematches.MatchReport'),
        ),
        migrations.AddField(
            model_name='matchorder',
            name='player',
            field=models.ForeignKey(to='leaguematches.Player'),
        ),
        migrations.AlterUniqueTogether(
            name='matchreport',
            unique_together=set([('played_date', 'reporter', 'opponent')]),
        ),
        migrations.AlterUniqueTogether(
            name='matchorder',
            unique_together=set([('player', 'match')]),
        ),
    ]
