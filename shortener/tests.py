from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from .models import Shorturl
from .utils import generate_slug, extract_domain_prefix
from .rate_limiter import check_rate_limit

class TestExtractDomainPrefix(TestCase):
    def test_extracts_youtube(self):
        url = "https://www.youtube.com/watch?v=abc123"
        self.assertEqual(extract_domain_prefix(url), 'youtube')
    
    def test_extracts_github(self):
        url = "https://github.com/user/repo"
        self.assertEqual(extract_domain_prefix(url), 'github')
    
    def test_handles_invalid_urls(self):
        self.assertEqual(extract_domain_prefix("not-a-url"), '')

class GenerateSlug(TestCase):
    def test_slug_contains_domain_prefix(self):
        slug = generate_slug("https://www.youtube.com/watch?v=abc")
        self.assertTrue(slug.startswith('youtube-'))
    
    def test_slug_is_unique(self):
        slug1 = generate_slug("https://www.github.com")
        slug2 = generate_slug("https://www.github.com")
        self.assertNotEqual(slug1, slug2)

class TestRateLimiter(TestCase):
    def test_allows_request_under_limit(self):
        result = check_rate_limit(user_id=999)
        self.assertTrue(result)
    
    def test_blocks_after_limit_exceeded(self):
        with patch('shortener.rate_limiter.RATE_LIMIT', 2):
            check_rate_limit(user_id=888)
            check_rate_limit(user_id=888)
            result = check_rate_limit(user_id=888)
            self.assertFalse(result)

class TestShorturlModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_short_url(self):
        url = Shorturl.objects.create(
            user=self.user,
            original_url='https://www.google.com',
            slug='google-abc1'
        )
        self.assertEqual(url.clickcount, 0)
        self.assertTrue(url.is_active)

    def test_str_representation(self):
        url = Shorturl.objects.create(
            user=self.user,
            original_url='https://www.google.com',
            slug='google-abc2'
        )
        self.assertIn('google-abc2', str(url))