from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'

router_v1 = DefaultRouter()

router_v1.register(r'users/subscriptions', views.UserViewSet, basename='subscriptions')

urlpatterns = [
    path('', include(router_v1.urls)),
    #path('users/subscriptions/', views.UserViewSet),
    path('users/<int:pk>/subscribe/', views.subscribe),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
]
