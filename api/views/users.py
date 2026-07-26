from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers import UserSerializer, UserCreateSerializer, UserPreferencesSerializer
from api.permissions import IsSelfOrAdmin
from .schemas import USER_VIEWSET_SCHEMA


@USER_VIEWSET_SCHEMA
class UserViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing User accounts and their associated preferences.
    """
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsSelfOrAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'me_preferences':
            return UserPreferencesSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'me_preferences':
            return [IsAuthenticated()]
        return [IsSelfOrAdmin()]

    @action(detail=False, methods=['get', 'patch'], url_path='me/preferences', permission_classes=[IsAuthenticated])
    def me_preferences(self, request):
        """
        Get or partially update preferences for the currently authenticated user.
        """
        preferences = request.user.preferences

        if request.method == 'GET':
            serializer = UserPreferencesSerializer(preferences)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            serializer = UserPreferencesSerializer(preferences, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

