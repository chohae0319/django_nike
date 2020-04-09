from django.contrib import admin
from .models import Order, OrderList, Shipping

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderList)
admin.site.register(Shipping)