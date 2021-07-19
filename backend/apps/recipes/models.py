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
    tags = models.ManyToManyField(Tag, related_name='tags', through='TagRecipe')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredient',
                                         through='IngredientRecipe')
    is_favorited = models.BooleanField()
    is_in_shopping_cart = models.BooleanField()
    name = models.CharField(max_length=256)
    image = models.ImageField(
        upload_to='apps/recipes/images/',
        blank=True,
        null=True
    )
    text = models.TextField()
    cooking_time = models.IntegerField()

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.CharField(max_length=64)


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'
