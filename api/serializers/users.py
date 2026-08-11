from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from api.models import UserPreferences


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['temperature_unit', 'email_notifications', 'summary_frequency', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    preferences = UserPreferencesSerializer(required=False)
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'preferences']
        read_only_fields = ['id', 'username', 'is_active', 'is_staff', 'date_joined']

    def validate_password(self, value):
        if value:
            validate_password(value, user=self.instance)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        preferences_data = validated_data.pop('preferences', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if preferences_data and hasattr(instance, 'preferences'):
            pref_serializer = UserPreferencesSerializer(
                instance.preferences, data=preferences_data, partial=True
            )
            pref_serializer.is_valid(raise_exception=True)
            pref_serializer.save()

        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
