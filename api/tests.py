from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserPreferences


class HealthCheckTest(APITestCase):
    def test_health_check_endpoint(self):
        url = reverse('api:health_check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')
        self.assertIn('message', response.data)

    def test_root_redirects_to_swagger(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/api/schema/swagger-ui/')

    def test_automatic_user_preferences_creation(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertTrue(hasattr(user, 'preferences'))
        self.assertEqual(user.preferences.temperature_unit, 'C')
        self.assertEqual(user.preferences.summary_frequency, 'daily')
