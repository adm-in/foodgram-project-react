from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'recipes'

router_v1 = DefaultRouter()

router_v1.register(r'recipes', views.RecipeViewSet, basename='recipes')
router_v1.register(
    r'ingredients', views.IngredientViewSet, basename='ingredients'
)
router_v1.register(
    r'recipes/(?P<recipes_id>\d+)/favorite/',
    views.FavoriteViewSet,
    basename='favorite',
)
router_v1.register(
    r'recipes/download_shopping_cart/',
    views.PurchaseViewSet,
    basename='purchase',
)
urlpatterns = [
    path('', include(router_v1.urls)),
]
