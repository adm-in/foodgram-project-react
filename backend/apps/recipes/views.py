import django_filters.rest_framework
from django.db.models import Sum
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Purchase,
                            Recipe, Tag)
from recipes.paginators import CustomPageNumberPaginator
from recipes.permissions import AdminOrAuthorOrReadOnly
from recipes.serializers import (FavoriteSerializer, GetRecipeSerializer,
                                 IngredientSerializer, PostRecipeSerializer,
                                 PurchaseSerializer, TagSerializer)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import (api_view, permission_classes,
                                       renderer_classes)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator
    permission_classes = [
        AdminOrAuthorOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return GetRecipeSerializer
        return PostRecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [
        AllowAny,
    ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = IngredientFilter


class IngredientRecipeViewSet(viewsets.ModelViewSet):
    queryset = IngredientRecipe.objects.all()
    serializer_class = GetRecipeSerializer
    permission_classes = [
        AllowAny,
    ]


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite(request, pk):
    if request.method == 'GET':
        qs = Recipe.objects.all()
        recipe = get_object_or_404(qs, id=pk)
        Favorite.objects.create(user_id=request.user.id, recipe_id=pk)
        serializer = FavoriteSerializer(data=recipe)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    favorite_qs = Favorite.objects.all()
    favorite_recipe = get_object_or_404(favorite_qs, recipe_id=pk)
    favorite_recipe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def purchase(request, pk):
    if request.method == 'GET':
        qs = Recipe.objects.all()
        recipe = get_object_or_404(qs, id=pk)
        Purchase.objects.create(user_id=request.user.id, recipe_id=pk)
        serializer = PurchaseSerializer(data=recipe)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    purchase_qs = Purchase.objects.all()
    purchase_recipe = get_object_or_404(purchase_qs, recipe_id=pk)
    purchase_recipe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class MyUserRenderer(CSVRenderer):
    header = ['???????????????? ??????????????????????', '????????????????????', '?????????????? ??????????????????']


@api_view(['GET'])
@renderer_classes((MyUserRenderer,))
@permission_classes([IsAuthenticated])
def export_purchase(request):
    purchases = (
        IngredientRecipe.objects.filter(recipe__purchases__user=request.user)
        .values('ingredient__name', 'ingredient__measurement_unit')
        .annotate(total_amount=Sum('amount'))
    )
    content = [
        {
            '???????????????? ??????????????????????': purchase['ingredient__name'],
            '????????????????????': purchase['total_amount'],
            '?????????????? ??????????????????': purchase['ingredient__measurement_unit'],
        }
        for purchase in purchases
    ]
    return Response(content)
