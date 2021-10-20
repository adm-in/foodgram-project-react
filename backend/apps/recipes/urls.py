from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes import views

app_name = 'recipes'

router_v1 = DefaultRouter()

router_v1.register(r'recipes', views.RecipeViewSet, basename='recipes')
router_v1.register(r'tags', views.TagViewSet, basename='tags')
router_v1.register(
    r'ingredients', views.IngredientViewSet, basename='ingredients'
),

urlpatterns = [
    path('recipes/download_shopping_cart/', views.export_purchase),
    path('', include(router_v1.urls)),
    path('recipes/<int:pk>/favorite/', views.favorite),
    path('recipes/<int:pk>/shopping_cart/', views.purchase),
]
