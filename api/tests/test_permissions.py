from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class PermissionsTest(APITestCase):
    """
    Tests for IsSelfOrAdmin custom permissions class.
    """

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', 
            password='Password123', 
            email='user1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            password='Password123', 
            email='user2@example.com'
        )
        self.admin = User.objects.create_superuser(
            username='adminuser', 
            password='AdminPassword123', 
            email='admin@example.com'
        )

    def test_user_list_unauthenticated(self):
        url = reverse('api:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_as_regular_user(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('api:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_access_other_user_profile(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:user-detail', kwargs={'pk': self.user2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update_other_user_profile(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:user-detail', kwargs={'pk': self.user2.pk})
        response = self.client.patch(url, {'first_name': 'Hacked'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_any_user_profile(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('api:user-detail', kwargs={'pk': self.user1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
