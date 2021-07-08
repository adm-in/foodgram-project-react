from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    unit = models.CharField(max_length=64)

    def __str__(self):
        return '{}, {}'.format(self.name, self.unit)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe')

    def __str__(self):
        return self.title


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.IntegerField()
