from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid


class Results(models.Model):
    # id_uui = models.IntegerField(max_length=20) # models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Time = models.IntegerField(max_length=20)
    PartId = models.IntegerField(max_length=20)
    ComponentId = models.IntegerField(max_length=20)
    Name = models.CharField(max_length=30)
    # product_type = models.CharField(max_length=50)
    # price = models.IntegerField(max_length=20)

    # Result = JSONField()

    def __str__(self):
        return self.name

