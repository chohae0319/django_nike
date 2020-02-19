from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model): # 내가 주문한 아이템
    # product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    # def __str__(self):
    #     return self.product.name

class Order(models.Model): # 카트에 들어 있는 아이템
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{} - {}'.format(self.owner, self.ref_code)