# pyrefly: ignore [missing-import]
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

@extend_schema(
    summary="Health Check Endpoint",
    description="Returns API status, application name, and system health information.",
    responses={
        200: inline_serializer(
            name='HealthCheckResponse',
            fields={
                'status': serializers.CharField(),
                'message': serializers.CharField(),
                'version': serializers.CharField(),
            }
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Verifica el estado del servicio API.
    """
    return Response(
        {
            'status': 'ok',
            'message': 'WeatherFlow API está funcionando correctamente.',
            'version': '1.0.0'
        },
        status=status.HTTP_200_OK
    )
