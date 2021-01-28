import uuid
from time import time

from django.db import models
from django.contrib.auth import get_user_model

from pytils.translit import slugify


def gen_slug(s):
    slug = slugify(s)
    return slug + '-' + str(int(time()))

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, primary_key=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', null=True, blank=True)


    def __str__(self):
        return self.name

    def save(self):
        if not self.slug:
            self.slug = gen_slug(self.name)
        super().save()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, blank=True)
    product_name  = models.CharField(max_length=50)
    calories      = models.DecimalField(max_digits=5, decimal_places=2)
    fats          = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)
    proteins      = models.DecimalField(max_digits=5, decimal_places=2)
    categories    = models.ManyToManyField(Category, related_name='categories')

    def __str__(self):
        return self. product_name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        super().save(*args, **kwargs)

    
    class Meta:
        ordering = ('calories', )



class ProductImage(models.Model):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product,
                                related_name='images',
                                on_delete=models.CASCADE)



