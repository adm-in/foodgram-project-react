from djoser.serializers import UserCreateSerializer as DjoserUserCreate
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from rest_framework import serializers
from users.models import CustomUser, Subscribe


class UserCreateSerializer(DjoserUserCreate):
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
    image = Base64ImageField(
        max_length=None, required=True, allow_empty_file=False, use_url=True,
    )

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

    def get_is_subscribed(self, user):
        return user.follower.all().exists()


class SubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
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

    def get_is_subscribed(self, user):
        return user.follower.all().exists()

    def get_recipes_count(self, recipe):
        return recipe.recipe_set.count()

    def get_recipes(self, user):
        from recipes.serializers import GetRecipeSerializer

        queryset = Recipe.objects.filter(author=user)[:3]
        return GetRecipeSerializer(queryset, many=True).data


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'

    def to_representation(self, instance):
        subscriptions = CustomUser.objects.filter(follower=instance)
        serializer = SubscribeSerializer(subscriptions, many=True)
        return serializer.data
