from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .schemas import HEALTH_CHECK_SCHEMA


@HEALTH_CHECK_SCHEMA
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Verifies API service status.
    """
    return Response(
        {
            'status': 'ok',
            'message': 'WeatherFlow API is working correctly.',
            'version': '1.0.0'
        },
        status=status.HTTP_200_OK
    )
