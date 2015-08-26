from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from accounts.models import UserAccount, UserContact
from accounts.serializers import UserAccountSerializer, UserContactSerializer


class AccountContactsViewSet(viewsets.ModelViewSet):
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        skip_fields = [self.pagination_class.page_query_param, self.pagination_class.page_size_query_param]
        params = {}
        for field_name in self.request.query_params:
            if field_name in skip_fields:
                continue

            params[field_name] = self.request.query_params.get(field_name)

        return UserContact.objects.filter(**params)


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        skip_fields = [self.pagination_class.page_query_param, self.pagination_class.page_size_query_param]
        params = {}
        for field_name in self.request.query_params:
            if field_name in skip_fields:
                continue

            params[field_name] = self.request.query_params.get(field_name)

        return UserAccount.objects.filter(**params)
