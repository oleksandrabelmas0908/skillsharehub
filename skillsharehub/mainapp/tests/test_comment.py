from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

import logging

from skillsharehub.mainapp.models import CustomUser, Chanel, Post, Comment


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CommentTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_comment_owner = CustomUser.objects.create_user(email="owner@example.com", first_name="Test", password="testpass")
        cls.chanel = Chanel.objects.create(name="Test Chanel", owner=cls.user_comment_owner)
        cls.post = Post.objects.create(title="Test Post", description="This is a test post.", video_link="http://example.com/video", chanel=cls.chanel)
        cls.comment = Comment.objects.create(content="This is a test comment.", post=cls.post, author=cls.user_comment_owner)
        cls.another_user = CustomUser.objects.create_user(email="another@example.com", first_name="Another", password="anotherpass")

    def test_comment_list(self):
        url = reverse('comment_post_list', kwargs={'post_pk': self.post.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_manage_create(self):
        url = reverse('comment_manage', kwargs={'post_pk': self.post.pk})
        data = {
            'content': 'This is a new comment.',
            'post': str(self.post.pk)
        }
        self.client.force_authenticate(user=self.user_comment_owner)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_manage_create_unauthenticated(self):
        url = reverse('comment_manage', kwargs={'post_pk': self.post.pk})
        data = {
            'content': 'This is a new comment.',
            'post': str(self.post.pk)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_manage_delete(self):
        url = reverse('comment_manage_delete', kwargs={'pk': self.comment.pk})
        self.client.force_authenticate(user=self.user_comment_owner)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_manage_delete_not_owner(self):
        url = reverse('comment_manage_delete', kwargs={'pk': self.comment.pk})
        self.client.force_authenticate(user=self.another_user)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)