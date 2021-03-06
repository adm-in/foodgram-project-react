from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework import serializers
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class PostIngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )


class GetIngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class GetRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = GetIngredientRecipeSerializer(
        many=True, source='recipe_ingredients',
    )
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'author',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
        )

    def get_is_favorited(self, recipe):
        return recipe.favorite_recipe.all().exists()

    def get_is_in_shopping_cart(self, recipe):
        return recipe.purchases.all().exists()


class PostRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
    )
    ingredients = PostIngredientRecipeSerializer(many=True)
    image = Base64ImageField(
        max_length=None, required=True, allow_empty_file=False, use_url=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
            'image',
        )

    def decorator(func): # noqa
        def wrapper(*args, **kwargs):
            ingredients, recipe = func(*args, **kwargs)

            for ingredient in ingredients:
                current_ingredient, ingredient_amount = ingredient
                ingredient_id = ingredient[current_ingredient]['id']
                ingredient_amount = ingredient[ingredient_amount]
                get_ingredient = Ingredient.objects.get(id=ingredient_id)
                IngredientRecipe.objects.create(
                    ingredient=get_ingredient,
                    amount=ingredient_amount,
                    recipe=recipe,
                )
            return recipe
        return wrapper

    @decorator
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        return ingredients, recipe

    @decorator
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time,
        )

        IngredientRecipe.objects.filter(recipe=instance).delete()

        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')

        instance.save()
        return ingredients, instance

    def to_representation(self, instance):
        return GetRecipeSerializer(
            instance, context={'request': self.context.get('request')},
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
