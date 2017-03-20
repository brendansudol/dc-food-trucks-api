from django.contrib.postgres.fields import JSONField
from django.db import models


class ModelBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Truck(ModelBase):
    name = models.CharField(max_length=256, primary_key=True)
    handle = models.CharField(max_length=128, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    last_tweet = JSONField(null=True, blank=True)
    location = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
