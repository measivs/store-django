import os

from PIL import Image
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

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


class ProductTag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='products/')
    product_thumbnail = models.ImageField(upload_to='products/thumbnails/', editable=False, null=True, blank=True)
    slug = models.SlugField(unique=True)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    tag = models.ManyToManyField(ProductTag, related_name='tags')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Save the main product instance first
        super().save(*args, **kwargs)

        # Full image path
        img_path = self.product_image.path

        # Create a cropped thumbnail
        thumbnail_resolution = (306, 214)
        img = Image.open(img_path)
        img = img.resize(thumbnail_resolution, Image.LANCZOS)

        # Ensure the thumbnail directory exists
        thumbnail_dir = os.path.join(os.path.dirname(img_path), "thumbnails")
        os.makedirs(thumbnail_dir, exist_ok=True)  # Create directory if it doesn't exist

        # Save thumbnail with a different path
        thumbnail_path = os.path.join(thumbnail_dir, os.path.basename(img_path))
        img.save(thumbnail_path)

        # Save the thumbnail path in the product_thumbnail field
        self.product_thumbnail = f'products/thumbnails/{os.path.basename(img_path)}'
        super().save(update_fields=['product_thumbnail'])
