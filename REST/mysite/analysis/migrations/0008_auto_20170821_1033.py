# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0007_auto_20170821_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='Filter',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='result',
            name='Pipeline',
            field=models.CharField(default='', max_length=30),
        ),
    ]