from django.contrib import admin

from accounts.models import UserAccount, UserContact


class UserContactInline(admin.StackedInline):
    model = UserContact


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('id', 'name', 'language', 'balance', 'bonus_balance')
    search_fields = ['id', 'name']
    inlines = [
        UserContactInline
    ]
