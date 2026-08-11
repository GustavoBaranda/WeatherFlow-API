from unittest.mock import patch, MagicMock
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from api.services.weather_service import celsius_to_fahrenheit, get_current_weather, get_weather_forecast
from api.services.geocoding_service import search_cities, resolve_city_coordinates


class WeatherViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='weatheruser',
            password='Password123',
            email='weather@example.com',
            first_name='Weather',
            last_name='User'
        )

    def test_current_weather_unauthenticated(self):
        url = reverse('api:weather_current')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('requests.get')
    def test_current_weather_celsius(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'current_weather': {
                'temperature': 22.5,
                'windspeed': 15.0,
                'weathercode': 1
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        self.client.force_authenticate(user=self.user)
        url = reverse('api:weather_current')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unit'], 'C')
        self.assertEqual(response.data['temperature'], 22.5)

    @patch('requests.get')
    def test_current_weather_fahrenheit(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'current_weather': {
                'temperature': 20.0,
                'windspeed': 10.0,
                'weathercode': 0
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Update user preference to Fahrenheit
        self.user.preferences.temperature_unit = 'F'
        self.user.preferences.save()

        self.client.force_authenticate(user=self.user)
        url = reverse('api:weather_current')
        response = self.client.get(f"{url}?city=Madrid")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unit'], 'F')
        self.assertEqual(response.data['temperature'], celsius_to_fahrenheit(20.0))

    @patch('requests.get')
    def test_weather_forecast(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'daily': {
                'time': ['2026-08-11', '2026-08-12'],
                'temperature_2m_max': [25.0, 26.0],
                'temperature_2m_min': [15.0, 16.0],
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        self.client.force_authenticate(user=self.user)
        url = reverse('api:weather_forecast')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['forecast']), 2)
        self.assertEqual(response.data['forecast'][0]['temp_max'], 25.0)

    @patch('requests.get')
    def test_city_search_endpoint(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {
                    'name': 'Cordoba',
                    'country': 'Argentina',
                    'country_code': 'AR',
                    'latitude': -31.4135,
                    'longitude': -64.1810,
                    'timezone': 'America/Argentina/Cordoba'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        self.client.force_authenticate(user=self.user)
        url = reverse('api:city_search')
        response = self.client.get(f"{url}?q=Cordoba")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Cordoba')
        self.assertEqual(response.data['results'][0]['country'], 'Argentina')

    def test_city_search_empty_query(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:city_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_celsius_to_fahrenheit_converter(self):
        self.assertEqual(celsius_to_fahrenheit(0), 32.0)
        self.assertEqual(celsius_to_fahrenheit(100), 212.0)
