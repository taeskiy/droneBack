from django.contrib import admin
from apps.category.models import Category
from mptt.admin import DraggableMPTTAdmin


class CategoryAdmin(DraggableMPTTAdmin):
    readonly_fields = ('slug',)


admin.site.register(Category, CategoryAdmin)
