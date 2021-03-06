# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-20 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0008_auto_20170821_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='ComponentId',
        ),
        migrations.AddField(
            model_name='result',
            name='Filter2',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='result',
            name='Prediction',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='result',
            name='PartId',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='result',
            name='Pipeline',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='result',
            name='Rmse',
            field=models.FloatField(default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='result',
            name='Time',
            field=models.CharField(default='', max_length=30),
        ),
    ]
