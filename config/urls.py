"""
URL Configuration for WeatherFlow APP project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Redirección automática de la raíz a la documentación Swagger UI
    path('', RedirectView.as_view(url='/api/schema/swagger-ui/', permanent=False)),
    
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # OpenAPI 3 Schema & UI documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

