from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
    inline_serializer,
    OpenApiResponse,
    OpenApiParameter,
)
from rest_framework import serializers
from api.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserPreferencesSerializer,
    CurrentWeatherSerializer,
    WeatherForecastSerializer,
    CitySearchResultSerializer,
    NotificationSerializer,
)


HEALTH_CHECK_SCHEMA = extend_schema(
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


USER_VIEWSET_SCHEMA = extend_schema_view(
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
                            'username': 'gustavo_baranda',
                            'email': 'gustavo@example.com',
                            'first_name': 'Gustavo',
                            'last_name': 'Baranda',
                            'is_active': True,
                            'is_staff': False,
                            'date_joined': '2026-08-11T12:00:00Z',
                            'preferences': {
                                'temperature_unit': 'C',
                                'email_notifications': True,
                                'summary_frequency': 'daily',
                                'created_at': '2026-08-11T12:00:00Z',
                                'updated_at': '2026-08-11T12:00:00Z'
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
                    'username': 'gustavo_baranda',
                    'email': 'gustavo@example.com',
                    'first_name': 'Gustavo',
                    'last_name': 'Baranda',
                    'is_active': True,
                    'is_staff': False,
                    'date_joined': '2026-08-11T12:00:00Z',
                    'preferences': {
                        'temperature_unit': 'C',
                        'email_notifications': True,
                        'summary_frequency': 'daily',
                        'created_at': '2026-08-11T12:00:00Z',
                        'updated_at': '2026-08-11T12:00:00Z'
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
                    'username': 'gustavo_baranda',
                    'email': 'gustavo@example.com',
                    'password': 'PasswordSegura123!',
                    'first_name': 'Gustavo',
                    'last_name': 'Baranda'
                },
                request_only=True
            ),
            OpenApiExample(
                'User Registration Response',
                summary='Successful user creation response',
                value={
                    'id': 1,
                    'username': 'gustavo_baranda',
                    'email': 'gustavo@example.com',
                    'first_name': 'Gustavo',
                    'last_name': 'Baranda'
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
                    'first_name': 'Gustavo',
                    'last_name': 'Baranda',
                    'password': 'NewSecurePassword456!',
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
                    'username': 'gustavo_baranda',
                    'email': 'gustavo@example.com',
                    'first_name': 'Gustavo',
                    'last_name': 'Baranda',
                    'is_active': True,
                    'is_staff': False,
                    'date_joined': '2026-08-11T12:00:00Z',
                    'preferences': {
                        'temperature_unit': 'F',
                        'email_notifications': True,
                        'summary_frequency': 'weekly',
                        'created_at': '2026-08-11T12:00:00Z',
                        'updated_at': '2026-08-11T12:35:00Z'
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
                    'first_name': 'Gustavo',
                    'last_name': 'Baranda',
                    'preferences': {
                        'temperature_unit': 'F',
                        'email_notifications': True,
                        'summary_frequency': 'daily'
                    }
                },
                request_only=True
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


NOTIFICATION_VIEWSET_SCHEMA = extend_schema_view(
    list=extend_schema(
        summary="List user notifications",
        description="Retrieve all in-app notifications for the authenticated user.",
        responses={200: NotificationSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Retrieve notification detail",
        description="Get specific notification by ID.",
        responses={200: NotificationSerializer}
    ),
    unread_count=extend_schema(
        summary="Get unread notification count",
        description="Returns count of unread notifications for bell icon.",
        responses={200: inline_serializer(name='UnreadCountResponse', fields={'unread_count': serializers.IntegerField()})}
    ),
    mark_read=extend_schema(
        summary="Mark notification as read",
        description="Mark a single notification as read.",
        responses={200: NotificationSerializer}
    ),
    mark_all_read=extend_schema(
        summary="Mark all notifications as read",
        description="Mark all notifications of current user as read.",
        responses={200: inline_serializer(name='MarkAllReadResponse', fields={'message': serializers.CharField(), 'updated_count': serializers.IntegerField()})}
    ),
    generate_summary=extend_schema(
        summary="Generate weather summary notification",
        description="Generates an in-app weather report notification based on user preferred city & temperature unit.",
        parameters=[
            OpenApiParameter(name='city', description='Optional city override', required=False, type=str),
        ],
        responses={201: NotificationSerializer}
    )
)
