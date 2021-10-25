from django.urls import path, include
from rest_framework import urlpatterns

from rest_framework.routers import DefaultRouter

from recipe.views import TagViewset

app_name = "recipe"

router = DefaultRouter()
router.register("tags", TagViewset)

urlpatterns = [path("", include(router.urls))]
