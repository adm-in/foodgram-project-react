from requests import Response
from rest_framework import viewsets
from rest_framework.decorators import action
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

    @action(detail=True, url_path='favorite', methods=['get'])
    def favorite(self, request, pk):
        obj = self.get_object()
        return Response({'tags': obj.tags, 'name': obj.name})

    def get_serializer_class(self):
        if self.request.method == 'GET':
            print('THIS GET')
            return GetRecipeSerializer
        if self.request.method == 'POST' or self.request.method == 'PUT':
            print('THIS POST')
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
    queryset = Recipe.objects.all()
    serializer_class = FavoriteSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
