import requests
from typing import Dict, Any, Tuple

DEFAULT_CITIES: Dict[str, Tuple[float, float]] = {
    'buenos aires': (-34.6037, -58.3816),
    'madrid': (40.4168, -3.7038),
    'new york': (40.7128, -74.0060),
    'london': (51.5074, -0.1278),
    'tokyo': (35.6762, 139.6503),
    'santiago': (-33.4489, -70.6693),
    'mexico city': (19.4326, -99.1332),
}


def celsius_to_fahrenheit(celsius: float) -> float:
    return round((celsius * 9 / 5) + 32, 1)


def get_city_coordinates(city_name: str) -> Tuple[float, float, str]:
    normalized = city_name.strip().lower()
    if normalized in DEFAULT_CITIES:
        lat, lon = DEFAULT_CITIES[normalized]
        return lat, lon, city_name.title()
    # Default to Buenos Aires if city is unknown
    return DEFAULT_CITIES['buenos aires'][0], DEFAULT_CITIES['buenos aires'][1], city_name.title()


def get_current_weather(city: str = 'Buenos Aires', temp_unit: str = 'C') -> Dict[str, Any]:
    lat, lon, city_display = get_city_coordinates(city)
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

        return {
            'city': city_display,
            'temperature': temp_final,
            'unit': temp_unit,
            'windspeed_kmh': windspeed,
            'weather_code': weather_code,
            'coordinates': {'latitude': lat, 'longitude': lon},
            'source': 'Open-Meteo API',
        }
    except Exception as e:
        # Fallback response in case external API is unreachable
        temp_c = 20.0
        return {
            'city': city_display,
            'temperature': temp_c if temp_unit == 'C' else celsius_to_fahrenheit(temp_c),
            'unit': temp_unit,
            'windspeed_kmh': 12.0,
            'weather_code': 0,
            'coordinates': {'latitude': lat, 'longitude': lon},
            'source': 'Fallback Mock (Network Error)',
            'error': str(e)
        }


def get_weather_forecast(city: str = 'Buenos Aires', temp_unit: str = 'C') -> Dict[str, Any]:
    lat, lon, city_display = get_city_coordinates(city)
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

        return {
            'city': city_display,
            'unit': temp_unit,
            'forecast': forecast_list,
            'source': 'Open-Meteo API',
        }
    except Exception as e:
        return {
            'city': city_display,
            'unit': temp_unit,
            'forecast': [],
            'source': 'Fallback Mock (Network Error)',
            'error': str(e)
        }
