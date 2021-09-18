from recipes.models import Recipe
from rest_framework import serializers

from .models import CustomUser, Subscribe


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

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
            'recipes'
        )

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=obj).exists()
