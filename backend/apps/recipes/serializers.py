from rest_framework import serializers

from .models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe


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
        many=True, queryset=Tag.objects.all(),
    )
    ingredients = PostIngredientRecipeSerializer(many=True,)

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
        print('! TEST PRINT !')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            current_ingredient, ingredient_amount = ingredient
            print('INGREDIENTS ID =', ingredient[current_ingredient]['id'])
            print('INGREDIENTS AMOUNT =', ingredient[ingredient_amount])
            print('CURRENT INGREDIENT =', current_ingredient)
            ingredient_id = ingredient[current_ingredient]['id']
            ingredient_amount = ingredient[ingredient_amount]
            get_ingredient = Ingredient.objects.get(id=ingredient_id)
            print('GET INGREDIENT', get_ingredient)
            IngredientRecipe.objects.create(
                ingredient=get_ingredient,
                amount=ingredient_amount,
                recipe=recipe,
            )
        return recipe
