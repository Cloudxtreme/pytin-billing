from __future__ import unicode_literals

from django.contrib import admin

from dedicated.models import DedicatedServerOffer


@admin.register(DedicatedServerOffer)
class DedicatedServerOfferAdmin(admin.ModelAdmin):
    list_display = ['platform', 'cpu_count', 'cpu_name', 'ram_gb', 'hdd_count', 'hdd_gb', 'price', 'visible']
    search_fields = ['platform', 'cpu_name', 'cpu_count', 'ram_gb', 'hdd_gb', 'hdd_count', 'price']
    list_filter = ['platform', 'cpu_name', 'cpu_count', 'hdd_gb', 'hdd_count', 'ram_gb', 'visible']

    def get_cpu(self, instance):
        return "%sx%s" % (instance.cpu_count, instance.cpu_name)

    def get_hdd(self, instance):
        return "%sx%s Gb" % (instance.hdd_count, instance.hdd_gb)
