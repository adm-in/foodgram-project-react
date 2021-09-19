from recipes.models import Recipe
from rest_framework import serializers
from djoser.serializers import \
    UserCreateSerializer as DjoserUserCreateSerializer
from .models import CustomUser, Subscribe


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
        )


class GetRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id', 'name',
            'image',
            'cooking_time'
        )


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
        )


class SubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = GetRecipeSerializer(source='recipe_set', many=True)

    # recipes = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
            'recipes'
        )

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=obj).exists()

    # def get_recipes(self, obj):
    # return obj.recipes.all()
