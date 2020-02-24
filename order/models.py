from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.utils import timezone


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)      # 0: 결제완료, 1: 배송중, 2: 배송완료, 3: 주문취소
    total_price = models.IntegerField()
    # 받는 사람 정보
    receive_address = models.CharField(max_length=70, blank=True)
    receive_name = models.CharField(max_length=10, blank=True)
    receive_phone = models.CharField(max_length=11, blank=True)


class OrderList(models.Model):  # Order 모델에 대한 상세내역 담는 클래스
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    size = models.IntegerField()
    quantity = models.IntegerField()


