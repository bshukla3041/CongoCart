from django.contrib import admin

from .models import Category, Product, OrderItem, Address, Order, Payment

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Payment)