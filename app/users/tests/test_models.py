from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test create a new user with email is successfull"""
        email = "test@test.ru"
        password = "testpassword"

        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized"""
        email = "test@TEST.ru"
        user = User.objects.create_user(email=email)

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test user creation with no email raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(None)

    def test_create_superuser(self):
        """Test creating a new superuser"""
        superuser = User.objects.create_superuser("test@test.ru", "test")

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
