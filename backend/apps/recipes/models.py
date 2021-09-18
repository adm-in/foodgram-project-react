from django.contrib.auth import get_user_model
from django.db import models
from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    measurement_unit = models.CharField(max_length=64)

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class Tag(models.Model):
    name = models.CharField(max_length=7, unique=True, blank=True)
    color = models.CharField(max_length=7, unique=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe'
    )
    name = models.CharField(max_length=256)
    image = models.ImageField(
        upload_to='apps/recipes/images/', blank=True, null=True
    )
    text = models.TextField()
    cooking_time = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, related_name='recipe_ingredients', on_delete=models.CASCADE
    )
    amount = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe}'


class Purchase(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
