# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.models import PersonalData


class RuCenterContract(models.Model):
    """
    RuCenter contract (NIC-D).
    """
    CONTRACT_A = 'NIC-A'
    CONTRACT_D = 'NIC-D'
    CONTRACT_REG = 'NIC-REG'

    CONTRACT_TYPE = (
        (CONTRACT_A, _('Information partner')),
        (CONTRACT_D, _('Regular customer')),
        (CONTRACT_REG, _('Resell domains')),
    )

    personal_data = models.ForeignKey(PersonalData)
    created_at = models.DateTimeField(db_index=True, default=timezone.now, null=False)
    type = models.CharField(db_index=True, max_length=15, choices=CONTRACT_TYPE, default=CONTRACT_D)
    verified = models.BooleanField(db_index=True, default=False, null=False)


class RuCenterDomain(models.Model):
    """
    Domain, that was registered for the contract.
    """
    contract = models.ForeignKey(RuCenterContract)

    created_at = models.DateTimeField(db_index=True, default=timezone.now, null=False)
    domain = models.CharField(db_index=True, max_length=155, null=False)
