from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health_check, UserViewSet, current_weather_view, weather_forecast_view

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('weather/current/', current_weather_view, name='weather_current'),
    path('weather/forecast/', weather_forecast_view, name='weather_forecast'),
    path('', include(router.urls)),
]

