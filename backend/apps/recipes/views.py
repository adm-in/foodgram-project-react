from rest_framework import viewsets

from .permissions import IsAuthorOrReadOnly

from .models import IngredientRecipe, Recipe, Tag, Ingredient, Favorite, \
    Purchase
from .serializers import (GetIngredientRecipeSerializer, GetRecipeSerializer,
                          PostIngredientRecipeSerializer, PostRecipeSerializer,
                          TagSerializer, IngredientSerializer,
                          FavoriteSerializer, PurchaseSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

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


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
