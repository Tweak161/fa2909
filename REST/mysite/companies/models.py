# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Result(models.Model):
    Time = models.IntegerField(max_length=20)
    PartId = models.IntegerField(max_length=20)
    ComponentId = models.IntegerField(max_length=20)
    Name = models.CharField(max_length=30, default="")
    Algorithm = models.CharField(max_length=30, default="")

    def str(self):
        return self.name








