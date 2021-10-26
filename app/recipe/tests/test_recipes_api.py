import os
import tempfile

from PIL import Image

from rest_framework.test import APITestCase
from rest_framework import status

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
from recipe.tests.utils import (
    User,
    RECIPE_ULR,
    sample_ingridient,
    sample_tag,
    sample_reciepe,
    detail_recipe_url,
    upload_image_url,
)


class PublicRecipeTests(APITestCase):
    """Test unauthenticated recipe API access"""

    def login_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPE_ULR)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeTests(APITestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.user = User.objects.create_user("test@test.ru", "testpass")
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieveng a list of recipes"""
        sample_reciepe(user=self.user)
        sample_reciepe(user=self.user)
        sample_reciepe(user=self.user)
        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        res = self.client.get(RECIPE_ULR)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        user2 = User.objects.create_user("test2@test.ru", "testpass2")
        sample_reciepe(user=user2)
        sample_reciepe(user=self.user)
        sample_reciepe(user=self.user)

        recipes = Recipe.objects.filter(user=self.user).order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        res = self.client.get(RECIPE_ULR)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_detail_recipe_view(self):
        """Test viewing recipe detail"""
        recipe = sample_reciepe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingridiets.add(sample_ingridient(user=self.user))
        serializer = RecipeDetailSerializer(recipe)

        url = detail_recipe_url(recipe.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating basic recipe usig API"""
        payload = {"title": "Recipe Title", "time_minutes": 5, "price": 10.00}

        res = self.client.post(RECIPE_ULR, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """Test creating recipe with tags"""
        tag1 = sample_tag(user=self.user)
        tag2 = sample_tag(user=self.user, name="Sample tag 2")

        payload = {"title": "Recipe Title", "time_minutes": 5, "price": 10.00, "tags": [tag1.id, tag2.id]}

        res = self.client.post(RECIPE_ULR, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data["id"])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingridients(self):
        """Test creating recipe with tags"""
        ingridient1 = sample_ingridient(user=self.user)
        ingridient2 = sample_ingridient(user=self.user, name="Sample tag 2")

        payload = {
            "title": "Recipe Title",
            "time_minutes": 10,
            "price": 15.00,
            "ingridiets": [ingridient1.id, ingridient2.id],
        }

        res = self.client.post(RECIPE_ULR, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data["id"])
        tags = recipe.ingridiets.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(ingridient1, tags)
        self.assertIn(ingridient2, tags)

    def test_update_recipe_patch(self):
        """Test update recipe with patch method"""
        recipe = sample_reciepe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        tag1 = sample_tag(user=self.user, name="Sample tag1")

        payload = {"title": "Sample title2", "tags": [tag1.id]}
        url = detail_recipe_url(recipe.id)

        self.client.patch(url, payload)

        recipe.refresh_from_db()
        tags = recipe.tags.all()
        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(tags.count(), 1)
        self.assertIn(tag1, tags)

    def test_update_recipe_put(self):
        """Test full update recipe with put method"""
        recipe = sample_reciepe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))

        payload = {"title": "Sample title2", "time_minutes": 123, "price": 12.00}
        url = detail_recipe_url(recipe.id)

        self.client.put(url, payload)

        recipe.refresh_from_db()
        tags = recipe.tags.all()

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))
        self.assertEqual(tags.count(), 0)


class RecipeUploadTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test@test.ru", "testpass")
        self.client.force_authenticate(self.user)
        self.recipe = sample_reciepe(user=self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image_to_recipe(self):
        """Test uploading image to recipe successfull"""
        url = upload_image_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)

            res = self.client.post(url, {"image": ntf}, format="multipart")

        self.recipe.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image"""
        url = upload_image_url(self.recipe.id)
        res = self.client.post(url, {"image": "notimage"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
