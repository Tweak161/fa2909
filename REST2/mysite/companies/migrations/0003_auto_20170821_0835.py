# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20170821_0830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='Name',
        ),
        migrations.AddField(
            model_name='result',
            name='RMSE',
            field=models.IntegerField(default=None, max_length=20),
        ),
    ]
