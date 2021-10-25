from rest_framework import serializers
from recipe.models import Recipe, Tag, Ingridient


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class IngridientSerializer(serializers.ModelSerializer):
    """Serializer for ingridient object"""

    class Meta:
        model = Ingridient
        fields = ("id", "name")
        read_only_fields = ("id",)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe object"""

    ingridiets = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingridient.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ("id",)


class RecipeDetailSerializer(RecipeSerializer):
    """Serilizer for recipe detail"""

    ingridiets = IngridientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
