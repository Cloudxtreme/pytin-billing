from __future__ import unicode_literals

from rest_framework import serializers

from dedicated.models import DedicatedServerOffer


class DedicatedServerOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = DedicatedServerOffer
