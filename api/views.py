from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, inline_serializer
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
    },
    examples=[
        OpenApiExample(
            'Health Check Response',
            summary='Example response returning API status and version',
            value={
                'status': 'ok',
                'message': 'WeatherFlow API is working correctly.',
                'version': '1.0.0'
            },
            response_only=True
        )
    ]
)

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


from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsSelfOrAdmin


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Retrieve a list of registered users. Requires authentication.",
        examples=[
            OpenApiExample(
                'Paginated Users List Response',
                summary='Sample paginated list response',
                value={
                    'count': 1,
                    'next': None,
                    'previous': None,
                    'results': [
                        {
                            'id': 1,
                            'username': 'johndoe',
                            'email': 'johndoe@example.com',
                            'first_name': 'John',
                            'last_name': 'Doe',
                            'is_active': True,
                            'is_staff': False,
                            'date_joined': '2026-07-22T20:00:00Z',
                            'preferences': {
                                'temperature_unit': 'C',
                                'email_notifications': True,
                                'summary_frequency': 'daily',
                                'created_at': '2026-07-22T20:00:00Z',
                                'updated_at': '2026-07-22T20:00:00Z'
                            }
                        }
                    ]
                },
                response_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Get user details",
        description="Retrieve profile details and preferences of a specific user.",
        examples=[
            OpenApiExample(
                'User Details Response',
                summary='Sample user profile and preferences',
                value={
                    'id': 1,
                    'username': 'johndoe',
                    'email': 'johndoe@example.com',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'is_active': True,
                    'is_staff': False,
                    'date_joined': '2026-07-22T20:00:00Z',
                    'preferences': {
                        'temperature_unit': 'C',
                        'email_notifications': True,
                        'summary_frequency': 'daily',
                        'created_at': '2026-07-22T20:00:00Z',
                        'updated_at': '2026-07-22T20:00:00Z'
                    }
                },
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Register new user",
        description="Register a new user account with initial default preferences.",
        examples=[
            OpenApiExample(
                'User Registration Payload',
                summary='Example request payload to register a new user',
                description='Valid sample data including password with uppercase, lowercase, and numbers.',
                value={
                    'username': 'johndoe',
                    'email': 'johndoe@example.com',
                    'password': 'SecurePassword123',
                    'first_name': 'John',
                    'last_name': 'Doe'
                },
                request_only=True
            ),
            OpenApiExample(
                'User Registration Response',
                summary='Successful user creation response',
                value={
                    'id': 1,
                    'username': 'johndoe',
                    'email': 'johndoe@example.com',
                    'first_name': 'John',
                    'last_name': 'Doe'
                },
                response_only=True,
                status_codes=['201']
            )
        ]
    ),
    update=extend_schema(
        summary="Update user profile",
        description="Update user information, password, and preferences.",
        examples=[
            OpenApiExample(
                'User Profile Update Payload',
                summary='Example update payload',
                value={
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'password': 'NewSecurePassword456',
                    'preferences': {
                        'temperature_unit': 'F',
                        'summary_frequency': 'weekly'
                    }
                },
                request_only=True
            )
        ]
    ),
    partial_update=extend_schema(summary="Partially update user profile", description="Partially update user fields or preferences."),
    destroy=extend_schema(summary="Delete user account", description="Delete a user account.")
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing User accounts and their associated preferences.
    """
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsSelfOrAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsSelfOrAdmin()]

