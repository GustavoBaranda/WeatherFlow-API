from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health_check, UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('', include(router.urls)),
]

