from django.contrib.auth import get_user_model
from django.test import client
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from recipe.models import Recipe, Tag, Ingridient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

User = get_user_model()
RECIPE_ULR = reverse("recipe:recipe-list")


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
        self.assertEqual(len(tags), 2)
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
        self.assertEqual(len(tags), 2)
        self.assertIn(ingridient1, tags)
        self.assertIn(ingridient2, tags)
