# coding=utf-8
from __future__ import unicode_literals

import traceback

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from domains.serializers import DomainOrderSerializer
from pybilling.settings import logger


class DomainOrderViewSet(viewsets.GenericViewSet):
    serializer_class = DomainOrderSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            return Response(serializer.save())
        except Exception, ex:
            logger.error(ex)
            logger.error(traceback.format_exc())
            return Response(ex.message, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            return Response(serializer.save())
        except Exception, ex:
            logger.error(ex)
            logger.error(traceback.format_exc())
            return Response(ex.message, status=status.HTTP_400_BAD_REQUEST)
