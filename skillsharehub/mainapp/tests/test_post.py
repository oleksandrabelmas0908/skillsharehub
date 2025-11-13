from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

import logging

from skillsharehub.mainapp.models import CustomUser, Chanel, Post


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PostTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(email="test@example.com", first_name="Test", password="testpass")
        cls.chanel = Chanel.objects.create(name="Test Chanel", owner=cls.user)

    def test_post_list(self):
        url = reverse('chanel_post_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_detail(self):
        post = Post.objects.create(title="Test Post", description="This is a test post.", video_link="http://example.com/video", chanel=self.chanel)
        url = reverse('post_detail', kwargs={'pk': post.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_manage_create(self):
        url = reverse('post_manage')
        data = {
            'title': 'Test Post',
            'video_link': 'http://example.com/video',
            'description': 'This is a test post.',
            'chanel': str(self.chanel.pk)
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PostManageDetailTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_chanel_owner = CustomUser.objects.create_user(email="owner@example.com", first_name="Owner", password="ownerpass")
        cls.chanel = Chanel.objects.create(name="Owner's Chanel", owner=cls.user_chanel_owner)
        cls.post = Post.objects.create(title="Owner's Post", description="This is owner's post.", video_link="http://example.com/owner_video", chanel=cls.chanel)
        cls.url = reverse('post_manage_detail', kwargs={'pk': cls.post.pk})
        cls.other_user = CustomUser.objects.create_user(email="other@example.com", first_name="Other", password="otherpass")


    def test_post_manage_update(self):
        data = {
            'title': 'Updated Owner Post',
            'video_link': 'http://example.com/updated_owner_video',
            'description': 'This is updated owner post.'
        }
        self.client.force_authenticate(user=self.user_chanel_owner)
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info(response.data)
        self.assertEqual(response.data["title"], 'Updated Owner Post')

    def test_post_manage_patch(self):
        data = {
            'description': 'This is patched owner post.'
        }
        self.client.force_authenticate(user=self.user_chanel_owner)
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info(response.data)
        self.assertEqual(response.data["description"], 'This is patched owner post.')

    def test_post_manage_unauthorized_update(self):
        data = {
            'title': 'Hacked Post Title',
        }
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_manage_bad_user_patch(self):
        data = {
            'description': 'Hacked Description'
        }
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_manage_delete(self):
        self.client.force_authenticate(user=self.user_chanel_owner)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)