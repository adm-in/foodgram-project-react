from django.urls import include, path
from . import views

app_name = 'users'

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    #path('users/<int:pk>/subscribe/', views.subscribe),
    #path('users/subscriptions/', views.subscriptions),
]
