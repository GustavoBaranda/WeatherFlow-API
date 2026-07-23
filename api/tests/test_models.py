from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from api.models import UserPreferences


class ModelSignalsTest(APITestCase):
    """
    Tests for database models and signal handlers.
    """

    def test_automatic_user_preferences_creation(self):
        user = User.objects.create_user(username='testuser', password='Password123')
        self.assertTrue(hasattr(user, 'preferences'))
        self.assertEqual(user.preferences.temperature_unit, 'C')
        self.assertEqual(user.preferences.summary_frequency, 'daily')
        self.assertTrue(user.preferences.email_notifications)

    def test_user_preferences_str(self):
        user = User.objects.create_user(username='struser', password='Password123')
        self.assertEqual(str(user.preferences), 'Preferences for struser')
