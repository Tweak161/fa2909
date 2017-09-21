# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid


# Create your models here.
class Result(models.Model):
    Time = models.CharField(max_length=30, default="")
    PartId = models.IntegerField(default=1)
    Algorithm = models.CharField(max_length=30, default="")
    Rmse = models.FloatField(max_length=20, default=1)
    Pipeline = models.CharField(max_length=50, default="")
    Filter = models.CharField(max_length=30, default="")
    Prediction = models.IntegerField(default=1)

    def str(self):
        return self.ticker








