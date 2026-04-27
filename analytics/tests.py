from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from shortener.models import Shorturl
from .models import Click


class TestRedirectView(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.short_url = Shorturl.objects.create(
            user=self.user,
            original_url='https://www.google.com',
            slug='google-abc1'
        )

    def test_redirect_valid_slug(self):
        response = self.client.get('/google-abc1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://www.google.com')

    def test_redirect_invalid_slug(self):
        response = self.client.get('/invalid-slug/')
        self.assertEqual(response.status_code, 404)

    def test_click_is_logged(self):
        self.client.get('/google-abc1/')
        self.assertEqual(Click.objects.count(), 1)

    def test_click_count_increments(self):
        self.client.get('/google-abc1/')
        self.short_url.refresh_from_db()
        self.assertEqual(self.short_url.clickcount, 1)


class TestAnalyticsView(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.short_url = Shorturl.objects.create(
            user=self.user,
            original_url='https://www.google.com',
            slug='google-abc2'
        )
        self.client.force_authenticate(user=self.user)

    def test_analytics_returns_correct_data(self):
        Click.objects.create(
            short_url=self.short_url,
            ip_address='127.0.0.1',
            device='desktop',
            browser='Chrome',
            country='India'
        )
        response = self.client.get(f'/api/analytics/google-abc2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_clicks'], 0)
        self.assertEqual(response.data['by_device']['desktop'], 1)

    def test_analytics_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/analytics/google-abc2/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_access_others_analytics(self):
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.get('/api/analytics/google-abc2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)