# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from accounts.models import PersonalData


class RegistrarContract(models.Model):
    personal_data = models.OneToOneField(PersonalData, primary_key=True)
    created_at = models.DateTimeField(db_index=True, default=timezone.now, null=False)
    registrar = models.CharField(db_index=True, max_length=35)
    number = models.CharField(db_index=True, max_length=15)

    def __unicode__(self):
        return "%s (%s)" % (self.number, self.registrar)
