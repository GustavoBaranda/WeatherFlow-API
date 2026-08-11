from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework import serializers

from api.models import Notification
from api.serializers import NotificationSerializer
from api.services.weather_service import get_current_weather


class NotificationViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing user In-App notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Get unread notification count",
        description="Returns count of unread notifications for bell icon.",
        responses={200: inline_serializer(name='UnreadCountResponse', fields={'unread_count': serializers.IntegerField()})}
    )
    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Mark notification as read",
        description="Mark a single notification as read.",
        responses={200: NotificationSerializer}
    )
    @action(detail=True, methods=['patch'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Mark all notifications as read",
        description="Mark all notifications of current user as read.",
        responses={200: inline_serializer(name='MarkAllReadResponse', fields={'message': serializers.CharField(), 'updated_count': serializers.IntegerField()})}
    )
    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        updated_count = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response(
            {'message': 'All notifications marked as read.', 'updated_count': updated_count},
            status=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Generate weather summary notification",
        description="Generates an in-app weather report notification based on user preferred city & temperature unit.",
        parameters=[
            OpenApiParameter(name='city', description='Optional city override', required=False, type=str),
        ],
        responses={201: NotificationSerializer}
    )
    @action(detail=False, methods=['post'], url_path='generate-summary')
    def generate_summary(self, request):
        city = request.query_params.get('city', 'Buenos Aires')
        temp_unit = 'C'
        if hasattr(request.user, 'preferences'):
            temp_unit = request.user.preferences.temperature_unit

        weather_info = get_current_weather(city=city, temp_unit=temp_unit)
        city_name = weather_info.get('city', city)
        temp = weather_info.get('temperature', 20.0)
        unit = weather_info.get('unit', temp_unit)
        wind = weather_info.get('windspeed_kmh', 10.0)

        title = f"Weather Report: {city_name}"
        message = f"Currently in {city_name}: {temp}°{unit} with winds of {wind} km/h."

        notification = Notification.objects.create(
            user=request.user,
            title=title,
            message=message,
            notification_type='weather_summary',
            is_read=False
        )

        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
