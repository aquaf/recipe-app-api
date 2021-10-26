from django.views.generic import detail
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipe.models import Ingridient, Tag, Recipe
from recipe.serializers import (
    RecipeSerializer,
    TagSerializer,
    IngridientSerializer,
    RecipeDetailSerializer,
    RecipeImageSerializer,
)


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
        elif self.action == "upload_image":
            return RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, requst, pk=None):
        """Upload image to recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=requst.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

