from django.contrib import admin
from .models import Ingredient, Recipe, IngredientRecipe, Tag, TagRecipe


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class TagRecipeInline(admin.TabularInline):
    model = Recipe.tag.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInLine, TagRecipeInline)


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(Tag)
admin.site.register(TagRecipe)
