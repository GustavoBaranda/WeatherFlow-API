from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class JWTAuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='jwtuser',
            password='SecurePassword123',
            email='jwt@example.com'
        )

    def test_obtain_token_pair_success(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'jwtuser',
            'password': 'SecurePassword123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_pair_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'jwtuser',
            'password': 'WrongPassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_success(self):
        url_obtain = reverse('token_obtain_pair')
        obtain_res = self.client.post(url_obtain, {
            'username': 'jwtuser',
            'password': 'SecurePassword123'
        })
        refresh_token = obtain_res.data['refresh']

        url_refresh = reverse('token_refresh')
        response = self.client.post(url_refresh, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_authenticated_endpoint_with_jwt_bearer(self):
        url_obtain = reverse('token_obtain_pair')
        obtain_res = self.client.post(url_obtain, {
            'username': 'jwtuser',
            'password': 'SecurePassword123'
        })
        access_token = obtain_res.data['access']

        url_me = reverse('api:user-me-preferences')
        response = self.client.get(url_me, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['temperature_unit'], 'C')
