from __future__ import unicode_literals

from django.db import models


class DedicatedServerOffer(models.Model):
    platform = models.CharField(db_index=True, max_length=155)

    cpu_name = models.CharField(db_index=True, max_length=155)
    cpu_count = models.PositiveSmallIntegerField(db_index=True, default=1)

    ram_gb = models.PositiveSmallIntegerField(db_index=True)

    hdd_gb = models.PositiveSmallIntegerField(db_index=True)
    hdd_count = models.PositiveSmallIntegerField(db_index=True, default=1)

    price = models.PositiveIntegerField(db_index=True, default=0)

    visible = models.BooleanField(db_index=True, default=False)
    comment = models.TextField("Offer details", blank=True)
