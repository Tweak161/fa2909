# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-20 09:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0009_auto_20170920_0909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='Filter2',
        ),
    ]