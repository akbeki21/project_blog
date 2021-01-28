
# class RecipeImageInline(admin.TabularInline):
#     model = Recipe
#     max_num = 5
#     min_num = 1


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     inlines = [RecipeImageInline, ]


# admin.site.register(Like)

from django.contrib import admin

from .models import *


class ImageInline(admin.TabularInline):
    model = RecipeImage
    max_num = 4
    min_num = 1
    fields = ['image']

class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]
    list_display = ('author', 'text', 'created_at', 'recipe')

admin.site.register(Like)
admin.site.register(Recipe, RecipeAdmin)

