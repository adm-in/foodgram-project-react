from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Subscribe
from users.serializers import CustomUserSerializer, SubscribeSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return User.objects.all().order_by('id')


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscribe(request, pk):
    if request.method == 'GET':
        qs = User.objects.all()
        user = get_object_or_404(qs, id=pk)
        author_id = request.user.id
        user_id = User.objects.get(id=pk).id
        Subscribe.objects.create(author_id=author_id, user_id=user_id)
        serializer = SubscribeSerializer(data=user)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    subscribe_qs = Subscribe.objects.all()
    subscribe_recipe = get_object_or_404(subscribe_qs, user_id=pk)
    subscribe_recipe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(follower__author=user)
