from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class TestAuthEndpoints(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_register_success(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_register_weak_password(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': '123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_wrong_password(self):
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)