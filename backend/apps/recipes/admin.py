from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Purchase,
                            Recipe, Tag)


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class TagRecipeInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInLine, TagRecipeInline)
    list_display = (
        'id',
        'name',
        'author',
        'is_favorited',
    )
    list_filter = ('name', 'author', 'tags',)

    def is_favorited(self, obj):
        return obj.favorite_recipe.count()
    is_favorited.short_description = 'Количество добавлений в избранное'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'recipe',
        'amount'
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Purchase)
