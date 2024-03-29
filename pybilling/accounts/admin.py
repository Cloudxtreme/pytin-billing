from __future__ import unicode_literals

from django.contrib import admin

from accounts.models import UserAccount, UserContact, PersonalData, PersonalDataPerson, PersonalDataCompany, \
    PersonalDataEntrepreneur, PersonalDataForeignPerson, PersonalDataForeignCompany, PersonalDataForeignEntrepreneur


class UserContactInline(admin.StackedInline):
    model = UserContact
    extra = 0


class PersonalDataPersonInline(admin.StackedInline):
    model = PersonalDataPerson
    extra = 0


class PersonalDataEntrepreneurInline(admin.StackedInline):
    model = PersonalDataEntrepreneur
    extra = 0


class PersonalDataCompanyInline(admin.StackedInline):
    model = PersonalDataCompany
    extra = 0


class PersonalDataForeignPersonInline(admin.StackedInline):
    model = PersonalDataForeignPerson
    extra = 0


class PersonalDataForeignEntrepreneurInline(admin.StackedInline):
    model = PersonalDataForeignEntrepreneur
    extra = 0


class PersonalDataForeignCompanyInline(admin.StackedInline):
    model = PersonalDataForeignCompany
    extra = 0


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ['id', 'name', 'language', 'balance', 'bonus_balance']
    list_filter = ['language']
    search_fields = ['id', 'name', 'language']
    inlines = [
        UserContactInline,
    ]


@admin.register(PersonalData)
class PersonalDataAdmin(admin.ModelAdmin):
    search_fields = ['id', 'account__id', 'account__name', 'type']
    list_display = ['id', 'get_account_id', 'type', 'default', 'verified']
    list_filter = ['type', 'default', 'verified']
    raw_id_fields = ['account']

    inlines = [
        PersonalDataPersonInline,
        PersonalDataEntrepreneurInline,
        PersonalDataCompanyInline,
        PersonalDataForeignPersonInline,
        PersonalDataForeignEntrepreneurInline,
        PersonalDataForeignCompanyInline
    ]

    def get_account_id(self, instance):
        return instance.account.id

    get_account_id.short_description = 'Account ID'
    get_account_id.admin_order_field = 'account__id'
