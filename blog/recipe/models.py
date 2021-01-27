from django.db import models
from django.contrib.auth import get_user_model

from account.models import User

from django.contrib.auth import get_user_model


class Recipe(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recipe')
    text   = models.TextField()
    title  = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    recipe   = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    text       = models.TextField(max_length=400)
    author     = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.text} by {self.author}'


class RecipeImage(models.Model):
    image = models.ImageField(upload_to='recipe', blank=True, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe')


class Like(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.author