from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from accounts.views import AccountsViewSet, AccountContactsViewSet, PersonalDataViewSet

router = DefaultRouter()
router.register('accounts', AccountsViewSet)
router.register('contacts', AccountContactsViewSet)
router.register('pdata', PersonalDataViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
