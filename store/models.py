from enum import unique
from idlelib.pyparse import trans
from mptt.models import MPTTModel, TreeForeignKey

from django.db import models

# Create your models here.

class Category(MPTTModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['category_name']

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='products/')
    slug = models.SlugField(unique=True)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)

    def __str__(self):
        return self.name
