from django.contrib import admin

from apps.order.models import Order, OrderProduct, OrderUser


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = ('id', 'imei', 'user', 'status')
    list_filter = ('status',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderUser)
