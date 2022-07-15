from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = None
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2'),
        }),
    )
    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('phone_number',)


admin.site.register(User, CustomUserAdmin)
