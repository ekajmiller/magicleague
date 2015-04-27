# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'leaguematches', '0001_initial'), (b'leaguematches', '0002_auto_20150426_0123'), (b'leaguematches', '0003_auto_20150426_0140'), (b'leaguematches', '0004_auto_20150426_0145'), (b'leaguematches', '0005_auto_20150426_0200'), (b'leaguematches', '0006_matchreport_season')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MatchReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_date', models.DateTimeField()),
                ('played_date', models.DateField()),
                ('win', models.BooleanField(choices=[(True, b'Win'), (False, b'Loss')])),
                ('verified', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullname', models.CharField(max_length=100)),
                ('shortname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='seasons',
            field=models.ManyToManyField(to=b'leaguematches.Season', blank=True),
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
            name='round',
            field=models.PositiveIntegerField(choices=[(1, b'Round 1'), (2, b'Round 2'), (3, b'Round 3'), (4, b'Round 4'), (5, b'Round 5')]),
        ),
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
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.EmailField(default='', unique=True, max_length=254),
            preserve_default=False,
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
        migrations.AddField(
            model_name='matchreport',
            name='season',
            field=models.ForeignKey(default=1, to='leaguematches.Season'),
            preserve_default=False,
        ),
    ]
