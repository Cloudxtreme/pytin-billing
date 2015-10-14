from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from dedicated.models import DedicatedServerOffer
from dedicated.serializers import DedicatedServerOfferSerializer


class DedicatedServerOfferViewSet(viewsets.ModelViewSet):
    queryset = DedicatedServerOffer.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = DedicatedServerOfferSerializer
