from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'

router_v1 = DefaultRouter()

router_v1.register(r'auth/users', views.CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
