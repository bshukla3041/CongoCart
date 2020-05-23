from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CongoUserProfile

CongoUser = get_user_model()


class CongoUserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'date_joined', 'last_login', 'is_admin',)
    search_fields = ('phone_number',)
    readonly_fields = ('date_joined', 'last_login',)

    list_filter = ('is_admin', 'is_active',)
    filter_horizontal = ()
    fieldsets = ()
    ordering = ('phone_number',)


admin.site.register(CongoUser, CongoUserAdmin)
admin.site.register(CongoUserProfile)

admin.site.unregister(Group)
