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
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=obj).exists()

    def get_recipes_count(self, obj):
        return obj.recipe_set.all().count()


class SubscriptionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = GetRecipeSerializer(source='recipe_set', many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes',   'recipes_count', #'test'

        )

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=obj).exists()

    def get_recipes_count(self, obj):
        return obj.recipe_set.all().count()

    #def to_representation(self, instance):
       # serializer = CustomUserSerializer(source='instance.user', many=True)
        #serializer.is_valid()
        #print('!!', serializer)
        #return serializer.data

