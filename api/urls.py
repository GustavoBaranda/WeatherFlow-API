from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health_check,
    UserViewSet,
    NotificationViewSet,
    current_weather_view,
    weather_forecast_view,
    city_search_view,
)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('weather/cities/search/', city_search_view, name='city_search'),
    path('weather/current/', current_weather_view, name='weather_current'),
    path('weather/forecast/', weather_forecast_view, name='weather_forecast'),
    path('', include(router.urls)),
]
