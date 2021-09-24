from rest_framework import status, viewsets
from rest_framework.decorators import (api_view, permission_classes,
                                       renderer_classes)
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer

from .models import (Favorite, Ingredient, IngredientRecipe, Purchase, Recipe,
                     Tag)
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, GetRecipeSerializer,
                          IngredientSerializer, PostRecipeSerializer,
                          PurchaseSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return PostRecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [
        AllowAny,
    ]


class IngredientRecipeViewSet(viewsets.ModelViewSet):
    queryset = IngredientRecipe.objects.all()
    serializer_class = GetRecipeSerializer
    permission_classes = [
        AllowAny,
    ]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [
        AllowAny,
    ]


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
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
        favorite_recipe = get_object_or_404(favorite_qs, recipe_id=pk)
        favorite_recipe.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def purchase(request, pk):
    if request.method == 'GET':
        qs = Recipe.objects.all()
        recipe = get_object_or_404(qs, id=pk)
        serializer = PurchaseSerializer(recipe)
        user = request.user
        author = recipe.author
        purchase_recipe = None
        try:
            purchase_recipe = Purchase.objects.get(recipe_id=pk)
        except:
            print('Рецепт уже добавлен в список покупок')
        if user != author and purchase_recipe is None:
            Purchase.objects.create(author_id=recipe.author.id, recipe_id=pk)
            serializer = PurchaseSerializer(data=recipe)
            if serializer.is_valid():
                serializer.save()
        return Response(serializer.data)

    if request.method == 'DELETE':
        purchase_qs = Purchase.objects.all()
        purchase_recipe = get_object_or_404(purchase_qs, recipe_id=pk)
        purchase_recipe.delete()
        return Response(status=status.HTTP_200_OK)


class MyUserRenderer(CSVRenderer):
    header = ['name', 'cooking_time']


@api_view(['GET'])
@renderer_classes((MyUserRenderer,))
@permission_classes([IsAuthenticated])
def export_purchase(request):
    purchases = Purchase.objects.all()
    content = [
        {
            'name': purchase.recipe.name,
            'cooking_time': purchase.recipe.cooking_time,
        }
        for purchase in purchases
    ]
    return Response(content)
