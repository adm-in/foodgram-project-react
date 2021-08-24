from rest_framework import serializers

from .models import IngredientRecipe, Recipe, Tag, TagRecipe, Ingredient


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
        many=True, source='recipe_ingredients'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            #'is_favorited',
            #'is_in_shopping_cart',
            'name',
            'author',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
        )


class PostRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    ingredients = PostIngredientRecipeSerializer(many=True, )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        return Recipe.objects.create(**validated_data)
