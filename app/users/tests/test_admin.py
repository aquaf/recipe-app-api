from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser("admin@admin.ru", "admin")
        self.client.force_login(self.admin_user)

        self.user = User.objects.create_user(email="user@user.ru", password="user", name="User")

    def test_users_listed(self):
        """Test that users are listed in admin users page"""
        url = reverse("admin:users_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse("admin:users_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_add_page(self):
        """Test that user add page works"""
        url = reverse("admin:users_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
