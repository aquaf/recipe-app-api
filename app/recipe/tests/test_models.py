from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from recipe.models import Tag

User = get_user_model()


def sample_user(email="test@test.ru", password="testpass"):
    return User.objects.create_user(email, password)


class RecipeTests(TestCase):
    def test_tag_str(self):
        """Test tag string representation"""
        tag = Tag.objects.create(user=sample_user(), name="Vegan")

        self.assertEqual(str(tag), tag.name)
