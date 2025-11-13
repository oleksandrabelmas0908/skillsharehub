from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

import logging

from skillsharehub.mainapp.models import CustomUser, Chanel


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ChanelTests(APITestCase):
    def test_chanel_list(self):
        url = reverse('chanel_show')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chanel_manage_create(self):
        url = reverse('chanel_manage_create')
        data = {
            'name': 'Test Chanel',
            'description': 'This is a test chanel.'
        }
        user = CustomUser.objects.create_user(email='testuser@example.com', first_name='Test', password='testpass')
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_chanel_manage_unauthenticated(self):
        url = reverse('chanel_manage_create')
        data = {
            'name': 'Test Chanel',
            'description': 'This is a test chanel.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChanelManageDetailTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email='testuser@example.com', first_name='Test', password='testpass'
        )
        cls.chanel = Chanel.objects.create(name='Test Chanel', owner=cls.user)
        cls.url = reverse('chanel_manage_detail', kwargs={'pk': cls.chanel.pk})

    def test_get_chanel_manage_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_chanel_manage(self):
        data = {
            'name': 'Updated Test Chanel',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], 'Updated Test Chanel')

    def test_patch_chanel_manage(self):
        data = {
            'name': 'This is an updated test chanel.'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], 'This is an updated test chanel.')

    def test_delete_chanel_manage(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_chanel_manage_detail(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChanelSubscribeTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_creator = CustomUser.objects.create_user(
            email='testuser@example.com', first_name='creator', password='testpass'
        )
        cls.chanel = Chanel.objects.create(name='Test Chanel', owner=cls.user_creator)
        cls.user_subscriber = CustomUser.objects.create_user(
            email='testuser2@example.com', first_name='subscriber', password='testpass'
        )

    def test_subscribe_chanel(self):
        url = reverse('subscribe_chanel', kwargs={'pk': self.chanel.pk})
        self.client.force_authenticate(user=self.user_subscriber)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user_subscriber, self.chanel.subscribers.all())

    def test_unsubscribe_chanel(self):
        url = reverse('unsubscribe_chanel', kwargs={'pk': self.chanel.pk})
        self.chanel.subscribers.add(self.user_subscriber)
        self.client.force_authenticate(user=self.user_subscriber)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user_subscriber, self.chanel.subscribers.all())
