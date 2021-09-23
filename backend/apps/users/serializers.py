from djoser.serializers import \
    UserCreateSerializer as DjoserUserCreateSerializer
from recipes.models import Recipe
from rest_framework import serializers

from .models import CustomUser, Subscribe


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class GetRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=obj).exists()


class SubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = GetRecipeSerializer(source='recipe_set', many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=obj).exists()

    def get_recipes_count(self, obj):
        return obj.recipe_set.all().count()


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'

    def to_representation(self, instance):
        subscriptions = CustomUser.objects.filter(follower=instance)
        serializer = SubscribeSerializer(subscriptions, many=True)
        return serializer.data
