from rest_framework.test import APITestCase
from rest_framework import status

from recipe.models import Tag
from recipe.serializers import TagSerializer
from recipe.tests.utils import User, TAG_URL


class PublicTagsApiTests(APITestCase):
    """Test public availible tags API"""

    def test_login_required(self):
        """Test that login required to retrieving tags"""
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(APITestCase):
    """Test the authorized users tags API"""

    def setUp(self):
        self.user = User.objects.create_user("test@test.ru", "testpass")
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieve tags"""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Desert")
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_tag_limited_to_user(self):
        """Test that tags returned only for tag owner user"""
        user2 = User.objects.create_user("test2@test.ru", "testpass")
        Tag.objects.create(user=user2, name="Fruit")
        tag = Tag.objects.create(user=self.user, name="Test tag")

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)

    def test_create_tag_successful(self):
        """Test creating new tag"""
        payload = {"name": "new tag"}
        res = self.client.post(TAG_URL, payload)

        exists = Tag.objects.filter(user=self.user, name=payload["name"]).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_tag_invalid_payload(self):
        """Test with creating tag with invalid payload faild"""
        payload = {"name": ""}

        res = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
