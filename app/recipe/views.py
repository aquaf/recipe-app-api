from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.models import Ingridient, Tag, Recipe
from recipe.serializers import RecipeSerializer, TagSerializer, IngridientSerializer, RecipeDetailSerializer


class BaseRecipeViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewset(BaseRecipeViewset):
    """Manage tags"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientViewSet(BaseRecipeViewset):
    """Manage Ingridients"""

    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage Recipes"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        """Return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RecipeDetailSerializer
        return self.serializer_class
