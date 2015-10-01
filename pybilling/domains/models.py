# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from accounts.models import PersonalData


class RegistrarContract(models.Model):
    personal_data = models.ForeignKey(PersonalData)
    created_at = models.DateTimeField(db_index=True, default=timezone.now, null=False)
    registrar = models.CharField(db_index=True, max_length=35)
    number = models.CharField(db_index=True, max_length=15)


class RegistrarDomain(models.Model):
    """
    Domain, that was registered for the contract.
    """
    contract = models.ForeignKey(RegistrarContract)

    created_at = models.DateTimeField(db_index=True, default=timezone.now, null=False)
    domain = models.CharField(db_index=True, max_length=155, null=False)
