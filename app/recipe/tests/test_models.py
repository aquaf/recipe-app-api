from unittest.mock import patch

from django.test import TestCase

from recipe.models import Tag, Ingridient, Recipe
from recipe.utils import recipe_image_file_path
from recipe.tests.utils import User, sample_user


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

    @patch("uuid.uuid4")
    def test_ricipe_filename_uuid(self, mock_uuid):
        """Test that image is saved to the correct location"""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = recipe_image_file_path(None, "myimage.jpg")

        expected_path = f"uploads/recipe/{uuid}.jpg"

        self.assertEqual(file_path, expected_path)
