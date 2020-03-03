from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.utils import timezone


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)               # 0: 결제완료, 1: 배송중, 2: 배송완료, 3: 주문취소
    amount = models.IntegerField()               # 상품 금액
    shipping_price = models.IntegerField()       # 배송비
    total_price = models.IntegerField()          # 총 결제 금액
    # 받는 사람 정보
    receive_address = models.CharField(max_length=70)
    receive_name = models.CharField(max_length=10)
    receive_phone = models.CharField(max_length=11)
    memo = models.CharField(max_length=100, blank=True)     # 배송요청사항

    def __str__(self):
        return '{}. {} - {}'.format(self.pk, self.order_date.strftime("%Y-%m-%d"), self.user_id)


class OrderList(models.Model):  # Order 모델에 대한 상세내역 담는 클래스
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    size = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return '{}({}) : {}'.format(self.order_id.pk, self.pk, self.product_id)

class Shipping(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    destination_nickname = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=100)
    receiver_address = models.CharField(max_length=100)