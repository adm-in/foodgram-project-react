from rest_framework import serializers

from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Recipe
