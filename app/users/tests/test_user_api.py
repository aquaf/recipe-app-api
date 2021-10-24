from django.test import TestCase, client
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

CREATE_USER_URL = reverse("users:create")
TOKER_URL = reverse("users:token")
ME_URL = reverse("users:me")


class PublicUserApiTests(TestCase):
    """Test users Api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successfull(self):
        """Test user creation with valid payload are successfull"""
        payload = {"email": "test@test.ru", "name": "testname", "password": "testpassword"}

        res = self.client.post(CREATE_USER_URL, payload)
        user = User.objects.get(**res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", res.data)
        self.assertTrue(user.check_password(payload["password"]))

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {"email": "test@test.ru", "name": "testname", "password": "testpassword"}
        User.objects.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short(self):
        """Test that user password must be more that 5 characters"""
        payload = {"email": "test@test.ru", "name": "testname", "password": "te"}
        res = self.client.post(CREATE_USER_URL, payload)
        check_user_exists = User.objects.filter(email=payload["email"])

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(check_user_exists)

    def test_create_token_for_existing_user(self):
        """Test token creation for existing user"""
        payload = {"email": "test@test.ru", "name": "testname", "password": "testpassword"}
        User.objects.create_user(**payload)
        res = self.client.post(TOKER_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credentials(self):
        """Test that token not created with invalid credentials"""
        payload = {"email": "test@test.ru", "name": "testname", "password": "testpassword"}
        wrong_payload = {"email": "test@test.ru", "password": "wrongpass"}
        User.objects.create_user(**payload)
        res = self.client.post(TOKER_URL, wrong_payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_not_existing_user(self):
        """Test that token not created if user doesnt exists"""
        payload = {"email": "test@test.ru", "password": "testpassword"}
        res = self.client.post(TOKER_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {"email": "test@.ru", "password": "testpassword"}
        res = self.client.post(TOKER_URL, payload)
        self.assertNotIn("token", res.data)

    def test_retrieve_user_me_url_unauthorized(self):
        """Test that authentication is required for users for me url"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test api request that require authentication"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru", password="testpass", name="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_me_url_success(self):
        """Test retrieve me url for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})

    def post_method_not_allowed(self):
        """Test that post method not allowed for me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test update user profile for authenticated user"""
        payload = {"name": "new_name", "password": "new_pass"}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
