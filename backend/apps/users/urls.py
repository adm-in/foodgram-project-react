from django.urls import include, path
from . import views

app_name = 'users'


urlpatterns = [
    path('users/subscriptions/', views.subscriptions),
    path('users/<int:pk>/subscribe/', views.subscribe),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
]
