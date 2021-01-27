from django.contrib import admin

from .models import Category, ProductImage, Product


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image']

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]
    list_display = ('product_name', 'calories', 'carbohydrates', 'fats', 'proteins')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

