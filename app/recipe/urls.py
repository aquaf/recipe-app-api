from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe.views import TagViewset, IngridientViewSet, RecipeViewSet

app_name = "recipe"

router = DefaultRouter()
router.register("tags", TagViewset)
router.register("ingridients", IngridientViewSet)
router.register("recipe", RecipeViewSet)

urlpatterns = [path("", include(router.urls))]