from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from recipes.models import Recipe

from .serializers import CustomUserSerializer, SubscribeSerializer, \
    GetRecipeSerializer, SubscriptionsSerializer
from .models import CustomUser, Subscribe
from rest_framework.response import Response


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = GetRecipeSerializer


@api_view(['GET', 'DELETE'])
def subscribe(request, pk):
    if request.method == 'GET':
        qs = CustomUser.objects.all()
        user = get_object_or_404(qs, id=pk)
        author_id = request.user.id
        print('REQUEST.USER.ID =', author_id)
        try:
            user_id = CustomUser.objects.get(id=pk).id
            print('USER_ID', user_id)
            Subscribe.objects.create(author_id=author_id, user_id=user_id)
        except:
            print('Вы уже подписаны на этого пользователя')
        serializer = SubscribeSerializer(user)
        return Response(serializer.data)

    if request.method == 'DELETE':
        subscribe_qs = Subscribe.objects.all()
        subscribe_recipe = get_object_or_404(subscribe_qs, user_id=pk)
        subscribe_recipe.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def subscriptions(request):
    qs = CustomUser.objects.all()
    #qs2 = Subscribe.objects.all()
    user = get_object_or_404(qs, id=request.user.id)

    subscribes = Subscribe.objects.filter(author_id=request.user.id)
    #user2 = CustomUser.objects.filter(qs, subscribes)
    #user2 = get_object_or_404(qs, user)
    print('Subsribes', subscribes)
    print('user', user)
    serializer = SubscriptionsSerializer(user)
    return Response(serializer.data)
