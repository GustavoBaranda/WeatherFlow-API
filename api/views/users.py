from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.serializers import UserSerializer, UserCreateSerializer
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
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsSelfOrAdmin()]
