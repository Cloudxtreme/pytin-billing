from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from domains.views import DomainOrderViewSet

router = DefaultRouter()
router.register(r'domain_orders', DomainOrderViewSet, base_name='domain_orders')

urlpatterns = [
    url(r'^', include(router.urls)),
]
