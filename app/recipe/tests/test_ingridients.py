from django.contrib.auth import get_user_model
from django.test import client
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import serializers, status

from recipe.models import Ingridient
from recipe.serializers import IngridientSerializer


User = get_user_model()
INGRIDIENT_URL = reverse("recipe:ingridient-list")


class PublicIngridientApi(APITestCase):
    """Test public availible ingridient API"""

    def test_login_required(self):
        """Test that login required to retrieve Ingridient endpoint"""
        res = self.client.get(INGRIDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngridientApi(APITestCase):
    """Test the authorized users Ingridient API"""

    def setUp(self):
        self.user = User.objects.create_user("test@test.ru", "testpass")
        self.client.force_authenticate(self.user)

    def test_retrieve_ingridients(self):
        """Test retrieve a list of ingridients"""
        Ingridient.objects.create(user=self.user, name="Ing1")
        Ingridient.objects.create(user=self.user, name="Ing2")
        ingridiets = Ingridient.objects.all().order_by("-name")
        serializer = IngridientSerializer(ingridiets, many=True)

        res = self.client.get(INGRIDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingridients_limited_to_user(self):
        """Test that ingridients for authenticated user are returned"""
        user2 = User.objects.create_user("test2@test.ru", "testpass")
        Ingridient.objects.create(user=user2, name="Ing1")
        ingridient = Ingridient.objects.create(user=self.user, name="Ing2")

        res = self.client.get(INGRIDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingridient.name)

    def test_create_ingridient_successful(self):
        """Test creating new ingridient"""
        payload = {"name": "new ingridient"}
        res = self.client.post(INGRIDIENT_URL, payload)

        exists = Ingridient.objects.filter(user=self.user, name=payload["name"]).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_tag_invalid_payload(self):
        """Test with creating ingridint with invalid payload faild"""
        payload = {"name": ""}

        res = self.client.post(INGRIDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
