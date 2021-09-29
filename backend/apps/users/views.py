from django.db import IntegrityError
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import Recipe
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser, Subscribe
from .serializers import (CustomUserSerializer, GetRecipeSerializer,
                          SubscribeSerializer, SubscriptionsSerializer)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscribe(request, pk):
    if request.method == 'GET':
        qs = User.objects.all()
        user = get_object_or_404(qs, id=pk)
        author_id = request.user.id
        serializer = SubscribeSerializer(user)
        try:
            user_id = User.objects.get(id=pk).id
            Subscribe.objects.create(author_id=author_id, user_id=user_id)
        except IntegrityError:
            print('Вы уже подписаны на этого пользователя')
        return Response(serializer.data)

    subscribe_qs = Subscribe.objects.all()
    subscribe_recipe = get_object_or_404(subscribe_qs, user_id=pk)
    subscribe_recipe.delete()
    return Response(status=status.HTTP_200_OK)


class SubscriptionsViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(follower__author=user)
