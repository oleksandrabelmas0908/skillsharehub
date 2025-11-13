from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class AuthTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'password': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["password"], data["password2"])
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)


    def test_register_user_password_mismatch(self):
        url = reverse('register')
        data = {
            'password': 'testpassword123',
            'password2': 'differentpassword',
            'email': 'testuser@example.com',    
            'first_name': 'Test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


    def test_registry_existed_user(self):
        url = reverse('register')
        user1_data = {
            'password': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
        }
        self.client.post(url, data=user1_data, format='json')

        user2_data = {
            'password': 'anotherpassword123',
            'password2': 'anotherpassword123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
        }
        response = self.client.post(url, data=user2_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
