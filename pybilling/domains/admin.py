# coding=utf-8
from __future__ import unicode_literals

from django.contrib import admin

from domains.models import RegistrarContract, RegistrarOrder


@admin.register(RegistrarContract)
class RegistrarContractAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ['personal_data', 'created_at', 'number', 'registrar']
    list_filter = ['registrar']
    search_fields = ['number', 'registrar']


@admin.register(RegistrarOrder)
class RegistrarOrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ['id', 'domain', 'created_at', 'is_prolong', 'prolong_years']
    list_filter = ['is_prolong']
    search_fields = ['domain']
