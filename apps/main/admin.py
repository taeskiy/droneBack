from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from apps.main.models import CollectionProducts, Banner, MainCollections, Faq


class CollectionProductsInline(admin.TabularInline):
    model = CollectionProducts
    extra = 0
    raw_id_fields = ('product',)


class CollectionsAdmin(admin.ModelAdmin):
    inlines = [CollectionProductsInline]


class FaqAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(Banner)
admin.site.register(MainCollections, CollectionsAdmin)
admin.site.register(Faq, FaqAdmin)
