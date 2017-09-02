# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Result(models.Model):
    Time = models.IntegerField(max_length=20)
    PartId = models.IntegerField(max_length=20)
    ComponentId = models.IntegerField(max_length=20)
    Algorithm = models.CharField(max_length=30, default="")
    Rmse = models.FloatField(max_length=20, default=1)
    Pipeline = models.CharField(max_length=30, default="")
    Filter = models.CharField(max_length=30, default="")

    def str(self):
        return self.ticker








