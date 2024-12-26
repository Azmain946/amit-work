from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(deliveryCharge)

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInline]

admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)





