from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    unit = models.CharField(max_length=64)

    def __str__(self):
        return '{}, {}'.format(self.name, self.unit)


class Tag(models.Model):
    name = models.CharField(max_length=7, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe')
    tag = models.ManyToManyField(Tag, through='TagRecipe')

    def __str__(self):
        return self.title


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.IntegerField()


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'
