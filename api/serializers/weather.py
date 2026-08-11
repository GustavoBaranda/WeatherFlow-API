from rest_framework import serializers


class CoordinatesSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class CurrentWeatherSerializer(serializers.Serializer):
    city = serializers.CharField(help_text="Name of the city")
    temperature = serializers.FloatField(help_text="Current temperature in user's preferred unit")
    unit = serializers.ChoiceField(choices=['C', 'F'], help_text="Temperature unit (C or F)")
    windspeed_kmh = serializers.FloatField(help_text="Wind speed in km/h")
    weather_code = serializers.IntegerField(help_text="WMO weather interpretation code")
    coordinates = CoordinatesSerializer()
    source = serializers.CharField(help_text="Data source provider")


class ForecastDaySerializer(serializers.Serializer):
    date = serializers.CharField(help_text="Forecast date YYYY-MM-DD")
    temp_max = serializers.FloatField(help_text="Maximum daily temperature")
    temp_min = serializers.FloatField(help_text="Minimum daily temperature")
    unit = serializers.ChoiceField(choices=['C', 'F'])


class WeatherForecastSerializer(serializers.Serializer):
    city = serializers.CharField(help_text="Name of the city")
    unit = serializers.ChoiceField(choices=['C', 'F'])
    forecast = ForecastDaySerializer(many=True)
    source = serializers.CharField(help_text="Data source provider")
