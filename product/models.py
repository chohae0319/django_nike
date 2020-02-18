from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    main_class = models.CharField(max_length=25, unique=False)
    sub_class = models.CharField(max_length=25, unique=False)
    shoes_sub = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return '{} : {} : {} : {}'.format(self.pk, self.main_class, self.sub_class, self.shoes_sub)

    def name(self):
        return '{} {} {}'.format(self.main_class, self.sub_class, self.shoes_sub)

class Product(models.Model):
    # 상품번호, 상품명, 상품가격, 카테고리번호, (총재고량), 출시일, 판매량, 썸네일 이미지
    name = models.CharField(max_length=30, unique=True)
    price = models.IntegerField()
    style = models.CharField(max_length=10, blank=True)    # 상품번호. 나중에 blank=false로 바꿀예정
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)  # 카테고리에 속한 상품 존재하면 카테고리 삭제 불가
    soldout = models.BooleanField(default=False)   # 재고 있으면 False, 품절이면 True
    release_date = models.DateField()
    sales = models.IntegerField(default=0)   # 판매량 default를 0으로
    thumbnail = models.ImageField(upload_to='product/thumbnail/')

    def __str__(self):
        return '{}'.format(self.name)


class Inventory(models.Model):
    # 상품번호, 사이즈, 재고
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)  # 재고 존재하면 상품 삭제 불가
    size = models.CharField(max_length=10)
    amount = models.IntegerField()

    def __str__(self):
        return '{}: {}'.format(self.product_id, self.size)


class ProductImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)  # 상품 삭제하면 이미지도 함께 삭제
    image = models.ImageField(upload_to='product/detailimage/')

    def __str__(self):
        return '{} image'.format(self.product_id)

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return '{} - {}'.format(self.user_id, self.inventory_id)