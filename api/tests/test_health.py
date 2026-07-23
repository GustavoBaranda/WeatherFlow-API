from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class HealthCheckTest(APITestCase):
    """
    Tests for system health check endpoint and API documentation redirects.
    """

    def test_health_check_endpoint(self):
        url = reverse('api:health_check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')
        self.assertIn('message', response.data)
        self.assertIn('version', response.data)

    def test_root_redirects_to_swagger(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/api/schema/swagger-ui/')
