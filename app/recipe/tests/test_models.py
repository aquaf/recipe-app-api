from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from recipe.models import Tag, Ingridient, Recipe

User = get_user_model()


def sample_user(email="test@test.ru", password="testpass"):
    return User.objects.create_user(email, password)


class RecipeTests(TestCase):
    def test_tag_str(self):
        """Test tag string representation"""
        tag = Tag.objects.create(user=sample_user(), name="Vegan")

        self.assertEqual(str(tag), tag.name)

    def test_ingridient_str(self):
        """Test ingridient string representation"""
        ingridient = Ingridient.objects.create(user=sample_user(), name="Cucumber")

        self.assertEqual(str(ingridient), ingridient.name)

    def test_recipe_str(self):
        """Test recipe string representation"""
        recipe = Recipe.objects.create(user=sample_user(), title="Recipe title", time_minutes=3, price=5.00)

        self.assertEqual(str(recipe), recipe.title)
