# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

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
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_num', models.PositiveIntegerField()),
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
            model_name='round',
            name='season',
            field=models.ForeignKey(to='leaguematches.Season'),
        ),
        migrations.AddField(
            model_name='player',
            name='seasons',
            field=models.ManyToManyField(to='leaguematches.Season'),
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
            field=models.ForeignKey(to='leaguematches.Round'),
        ),
    ]
