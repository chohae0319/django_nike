from django.db import models
from django.contrib.auth.models import User
from product.models import Inventory


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(blank=True)
    status = models.IntegerField()      # 0: 결제완료, 1: 배송중, 2: 배송완료 3: 결제중
    receive_address = models.CharField(max_length=70, blank=True)
    receiver = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=11, blank=True)


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    inventory_id = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    quantity = models.IntegerField()