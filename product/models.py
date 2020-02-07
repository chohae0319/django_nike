from django.db import models

# Create your models here.
class Category(models.Model):
    main_class = models.CharField(max_length=25, unique=True)
    sub_class = models.CharField(max_length=25, unique=True)
    shoes_sub = models.CharField(max_length=25, unique=True)


# class Product(models.Model):
    # 상품 번호, 상품명, 상품가격, (총 재고량), 출시일, 판매량, 썸네일 이미지