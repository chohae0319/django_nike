from django.contrib import admin
from .models import Order, OrderList

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderList)