from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404

from .permissions import IsAuthorOrReadOnly

from .models import IngredientRecipe, Recipe, Tag, Ingredient, Favorite, \
    Purchase
from .serializers import (GetIngredientRecipeSerializer, GetRecipeSerializer,
                          PostIngredientRecipeSerializer, PostRecipeSerializer,
                          TagSerializer, IngredientSerializer,
                          FavoriteSerializer, PurchaseSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    # permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return PostRecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientRecipeViewSet(viewsets.ModelViewSet):
    queryset = IngredientRecipe.objects.all()
    serializer_class = GetRecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


@api_view(['GET', 'DELETE'])
def favorite(request, pk):
    if request.method == 'GET':
        qs = Recipe.objects.all()
        recipe = get_object_or_404(qs, id=pk)
        serializer = FavoriteSerializer(recipe)
        user = request.user
        author = recipe.author
        favorite_recipe = None
        try:
            favorite_recipe = Favorite.objects.get(recipe_id=pk)
        except:
            print('Рецепт уже добавлен в избранное')
        if user != author and favorite_recipe is None:
            Favorite.objects.create(author_id=recipe.author.id, recipe_id=pk)
            serializer = FavoriteSerializer(data=recipe)
            if serializer.is_valid():
                serializer.save()
        return Response(serializer.data)

    if request.method == 'DELETE':
        favorite_qs = Favorite.objects.all()
        favorite_recipe = get_object_or_404(favorite_qs, id=pk)
        favorite_recipe.delete()
        return Response(status=status.HTTP_200_OK)


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
