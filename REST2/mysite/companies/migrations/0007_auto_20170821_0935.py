# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_auto_20170821_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='Rmse',
            field=models.FloatField(default=0, max_length=20),
        ),
    ]