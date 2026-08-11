from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from api.services.weather_service import get_current_weather, get_weather_forecast
from api.services.geocoding_service import search_cities
from api.serializers import (
    CurrentWeatherSerializer,
    WeatherForecastSerializer,
    CitySearchResultSerializer,
)


@extend_schema(
    summary="Search cities for autocompletion",
    description="Searches world cities by name using Open-Meteo Geocoding API.",
    parameters=[
        OpenApiParameter(name='q', description='Search query (e.g. Cordoba, Paris, Berlin)', required=True, type=str),
    ],
    responses={200: CitySearchResultSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def city_search_view(request):
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response({'results': []}, status=status.HTTP_200_OK)

    results = search_cities(query=query, count=5)
    return Response({'query': query, 'count': len(results), 'results': results}, status=status.HTTP_200_OK)


@extend_schema(
    summary="Get current weather",
    description="Fetches current weather for any city, formatted according to the authenticated user's preferred temperature unit (Celsius or Fahrenheit).",
    parameters=[
        OpenApiParameter(name='city', description='City name (e.g. Buenos Aires, Madrid, New York, Cordoba)', required=False, type=str),
    ],
    responses={200: CurrentWeatherSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_weather_view(request):
    city = request.query_params.get('city', 'Buenos Aires')
    
    temp_unit = 'C'
    if hasattr(request.user, 'preferences'):
        temp_unit = request.user.preferences.temperature_unit

    weather_data = get_current_weather(city=city, temp_unit=temp_unit)
    return Response(weather_data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Get weather forecast",
    description="Fetches 7-day weather forecast for any city, formatted according to the authenticated user's preferred temperature unit.",
    parameters=[
        OpenApiParameter(name='city', description='City name (e.g. Buenos Aires, Madrid, New York, Cordoba)', required=False, type=str),
    ],
    responses={200: WeatherForecastSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weather_forecast_view(request):
    city = request.query_params.get('city', 'Buenos Aires')
    
    temp_unit = 'C'
    if hasattr(request.user, 'preferences'):
        temp_unit = request.user.preferences.temperature_unit

    forecast_data = get_weather_forecast(city=city, temp_unit=temp_unit)
    return Response(forecast_data, status=status.HTTP_200_OK)
