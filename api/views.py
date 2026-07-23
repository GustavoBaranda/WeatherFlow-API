from django.contrib.auth.models import User
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, inline_serializer, OpenApiResponse

from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsSelfOrAdmin


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


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Retrieve a list of registered users. Requires admin authentication.",
        responses={
            200: UserSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided."),
            403: OpenApiResponse(description="You do not have permission to view the user list.")
        },
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
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided."),
            403: OpenApiResponse(description="You do not have permission to view this profile."),
            404: OpenApiResponse(description="User not found.")
        },
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
        responses={
            201: UserCreateSerializer,
            400: OpenApiResponse(description="Bad Request - Validation error in provided user data.")
        },
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
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Bad Request - Validation error in updated user data."),
            401: OpenApiResponse(description="Authentication credentials were not provided."),
            403: OpenApiResponse(description="You do not have permission to modify this user."),
            404: OpenApiResponse(description="User not found.")
        },
        examples=[
            OpenApiExample(
                'User Profile Update Payload',
                summary='Example update payload',
                value={
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'password': 'NewSecurePassword456',
                    'preferences': {
                        'temperature_unit': 'F',
                        'summary_frequency': 'weekly'
                    }
                },
                request_only=True
            ),
            OpenApiExample(
                'User Profile Update Response',
                summary='Example response after updating user profile',
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
                        'temperature_unit': 'F',
                        'email_notifications': True,
                        'summary_frequency': 'weekly',
                        'created_at': '2026-07-22T20:00:00Z',
                        'updated_at': '2026-07-22T20:05:00Z'
                    }
                },
                response_only=True,
                status_codes=['200']
            )
        ]
    ),
    partial_update=extend_schema(
        summary="Partially update user profile",
        description="Partially update user fields or preferences.",
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Bad Request - Validation error in updated user data."),
            401: OpenApiResponse(description="Authentication credentials were not provided."),
            403: OpenApiResponse(description="You do not have permission to modify this user."),
            404: OpenApiResponse(description="User not found.")
        },
        examples=[
            OpenApiExample(
                'User Profile Partial Update Payload',
                summary='Example partial update payload',
                value={
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'preferences': {
                        'temperature_unit': 'F',
                        'email_notifications': True,
                        'summary_frequency': 'daily'
                    }
                },
                request_only=True
            ),
            OpenApiExample(
                'User Profile Partial Update Response',
                summary='Example response after partial update',
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
                        'temperature_unit': 'F',
                        'email_notifications': True,
                        'summary_frequency': 'daily',
                        'created_at': '2026-07-22T20:00:00Z',
                        'updated_at': '2026-07-22T20:05:00Z'
                    }
                },
                response_only=True,
                status_codes=['200']
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete user account",
        description="Delete a user account. Requires authentication as the account owner or an admin.",
        responses={
            204: OpenApiResponse(description="User account deleted successfully."),
            401: OpenApiResponse(description="Authentication credentials were not provided."),
            403: OpenApiResponse(description="You do not have permission to delete this user account."),
            404: OpenApiResponse(description="User not found.")
        }
    )
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
