import requests
from typing import Dict, Any
from django.core.cache import cache
from .geocoding_service import resolve_city_coordinates

CURRENT_WEATHER_CACHE_TIMEOUT = 900  # 15 minutes
FORECAST_CACHE_TIMEOUT = 1800  # 30 minutes


def celsius_to_fahrenheit(celsius: float) -> float:
    return round((celsius * 9 / 5) + 32, 1)


def get_current_weather(city: str = 'Buenos Aires', temp_unit: str = 'C') -> Dict[str, Any]:
    city_key = city.strip().lower()
    cache_key = f"weather_current_{city_key}_{temp_unit}"
    cached_data = cache.get(cache_key)
    if cached_data:
        cached_data['cached'] = True
        return cached_data

    lat, lon, city_display = resolve_city_coordinates(city)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        current = data.get('current_weather', {})
        temp_c = current.get('temperature', 20.0)
        windspeed = current.get('windspeed', 0.0)
        weather_code = current.get('weathercode', 0)

        temp_final = temp_c if temp_unit == 'C' else celsius_to_fahrenheit(temp_c)

        result = {
            'city': city_display,
            'temperature': temp_final,
            'unit': temp_unit,
            'windspeed_kmh': windspeed,
            'weather_code': weather_code,
            'coordinates': {'latitude': lat, 'longitude': lon},
            'source': 'Open-Meteo API',
            'cached': False,
        }
        cache.set(cache_key, result, CURRENT_WEATHER_CACHE_TIMEOUT)
        return result
    except Exception as e:
        temp_c = 20.0
        return {
            'city': city_display,
            'temperature': temp_c if temp_unit == 'C' else celsius_to_fahrenheit(temp_c),
            'unit': temp_unit,
            'windspeed_kmh': 12.0,
            'weather_code': 0,
            'coordinates': {'latitude': lat, 'longitude': lon},
            'source': 'Fallback Mock (Network Error)',
            'cached': False,
            'error': str(e)
        }


def get_weather_forecast(city: str = 'Buenos Aires', temp_unit: str = 'C') -> Dict[str, Any]:
    city_key = city.strip().lower()
    cache_key = f"weather_forecast_{city_key}_{temp_unit}"
    cached_data = cache.get(cache_key)
    if cached_data:
        cached_data['cached'] = True
        return cached_data

    lat, lon, city_display = resolve_city_coordinates(city)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        daily = data.get('daily', {})
        dates = daily.get('time', [])
        max_temps = daily.get('temperature_2m_max', [])
        min_temps = daily.get('temperature_2m_min', [])

        forecast_list = []
        for i in range(min(len(dates), 7)):
            t_max = max_temps[i] if i < len(max_temps) else 25.0
            t_min = min_temps[i] if i < len(min_temps) else 15.0
            forecast_list.append({
                'date': dates[i],
                'temp_max': t_max if temp_unit == 'C' else celsius_to_fahrenheit(t_max),
                'temp_min': t_min if temp_unit == 'C' else celsius_to_fahrenheit(t_min),
                'unit': temp_unit
            })

        result = {
            'city': city_display,
            'unit': temp_unit,
            'forecast': forecast_list,
            'source': 'Open-Meteo API',
            'cached': False,
        }
        cache.set(cache_key, result, FORECAST_CACHE_TIMEOUT)
        return result
    except Exception as e:
        return {
            'city': city_display,
            'unit': temp_unit,
            'forecast': [],
            'source': 'Fallback Mock (Network Error)',
            'cached': False,
            'error': str(e)
        }
