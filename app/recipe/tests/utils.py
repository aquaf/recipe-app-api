

from django.contrib.auth import get_user_model
from django.urls import reverse

from recipe.models import Recipe, Tag, Ingridient


User = get_user_model()

TAG_URL = reverse("recipe:tag-list")
INGRIDIENT_URL = reverse("recipe:ingridient-list")
RECIPE_ULR = reverse("recipe:recipe-list")


def sample_user(email="test@test.ru", password="testpass"):
    return User.objects.create_user(email, password)


def detail_recipe_url(id) -> str:
    """Return recipe detail url"""
    return reverse("recipe:recipe-detail", args=[id])


def sample_tag(user, name="Sample Tag") -> Tag:
    """Create and return sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingridient(user, name="Sample Ingridient") -> Ingridient:
    """Create and return sample ingridient"""
    return Ingridient.objects.create(user=user, name=name)


def sample_reciepe(user, **kwargs) -> Recipe:
    """Create and return sample recipe"""
    payload = {"title": "Title", "time_minutes": 5, "price": 5.00}
    payload.update(kwargs)

    return Recipe.objects.create(user=user, **payload)


def upload_image_url(id) -> str:
    """Return url for recipe image upload"""
    return reverse("recipe:recipe-upload-image", args=[id])
