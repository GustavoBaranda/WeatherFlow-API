from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class UserViewsTest(APITestCase):
    """
    Tests for UserViewSet CRUD endpoints and user preferences actions.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='regularuser', 
            password='Password123', 
            email='user@example.com',
            first_name='Regular',
            last_name='User'
        )
        self.admin = User.objects.create_superuser(
            username='adminuser', 
            password='AdminPassword123', 
            email='admin@example.com'
        )

    def test_user_registration(self):
        url = reverse('api:user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        
        new_user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_user, 'preferences'))
        self.assertEqual(new_user.preferences.temperature_unit, 'C')

    def test_user_registration_password_missing_uppercase(self):
        url = reverse('api:user-list')
        data = {
            'username': 'noupper',
            'password': 'securepassword123',
            'first_name': 'No',
            'last_name': 'Upper'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_registration_password_missing_number(self):
        url = reverse('api:user-list')
        data = {
            'username': 'nonumber',
            'password': 'SecurePassword',
            'first_name': 'No',
            'last_name': 'Number'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_registration_missing_names(self):
        url = reverse('api:user-list')
        data = {
            'username': 'nonames',
            'password': 'SecurePassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)

    def test_user_retrieve_self(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'regularuser')
        self.assertIn('preferences', response.data)

    def test_user_update_profile_and_preferences(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:user-detail', kwargs={'pk': self.user.pk})
        data = {
            'first_name': 'Updated',
            'preferences': {
                'temperature_unit': 'F',
                'summary_frequency': 'weekly'
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['preferences']['temperature_unit'], 'F')
        self.assertEqual(response.data['preferences']['summary_frequency'], 'weekly')

    def test_user_update_password_valid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:user-detail', kwargs={'pk': self.user.pk})
        data = {'password': 'NewValidPassword456'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewValidPassword456'))

    def test_user_update_password_invalid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:user-detail', kwargs={'pk': self.user.pk})
        data = {'password': '123'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_delete(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('api:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_me_preferences_get(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:user-me-preferences')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['temperature_unit'], 'C')
        self.assertEqual(response.data['email_notifications'], True)

    def test_me_preferences_patch(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:user-me-preferences')
        data = {'temperature_unit': 'F', 'summary_frequency': 'weekly'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['temperature_unit'], 'F')
        self.assertEqual(response.data['summary_frequency'], 'weekly')
