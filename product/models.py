from django.db import models

# Create your models here.
class Category(models.Model):
    main_class = models.CharField(max_length=25, unique=True)
    sub_class = models.CharField(max_length=25, unique=True)
    shoes_sub = models.CharField(max_length=25, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=20, unique=True)