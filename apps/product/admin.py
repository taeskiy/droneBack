from django.contrib import admin
from apps.product.models import Product, ProductImage, Restaurant


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
