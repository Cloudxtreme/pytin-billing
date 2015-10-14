from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from dedicated.views import DedicatedServerOfferViewSet

router = DefaultRouter()
router.register('dedic_offer', DedicatedServerOfferViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
