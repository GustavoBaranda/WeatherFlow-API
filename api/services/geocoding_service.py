import requests
from typing import List, Dict, Any, Tuple
from django.core.cache import cache

DEFAULT_CITIES: Dict[str, Tuple[float, float, str]] = {
    'buenos aires': (-34.6037, -58.3816, 'Buenos Aires, Argentina'),
    'madrid': (40.4168, -3.7038, 'Madrid, Spain'),
    'new york': (40.7128, -74.0060, 'New York, United States'),
    'london': (51.5074, -0.1278, 'London, United Kingdom'),
    'tokyo': (35.6762, 139.6503, 'Tokyo, Japan'),
    'santiago': (-33.4489, -70.6693, 'Santiago, Chile'),
    'mexico city': (19.4326, -99.1332, 'Mexico City, Mexico'),
    'wilde': (-34.7000, -58.3167, 'Wilde, Argentina'),
}

GEOCODING_CACHE_TIMEOUT = 86400  # 24 hours


def search_cities(query: str, count: int = 5) -> List[Dict[str, Any]]:
    """
    Searches for cities matching query using Open-Meteo Geocoding API with caching.
    """
    if not query or len(query.strip()) < 2:
        return []

    query_key = ''.join(c if c.isalnum() else '_' for c in query.strip().lower())
    cache_key = f"geocoding_search_{query_key}_{count}"
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query.strip()}&count={count}&language=en&format=json"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = data.get('results', [])
        city_list = []
        for item in results:
            city_list.append({
                'name': item.get('name', ''),
                'country': item.get('country', ''),
                'country_code': item.get('country_code', ''),
                'latitude': item.get('latitude', 0.0),
                'longitude': item.get('longitude', 0.0),
                'timezone': item.get('timezone', 'UTC'),
                'display_name': f"{item.get('name', '')}, {item.get('country', '')}".strip(', ')
            })
        cache.set(cache_key, city_list, GEOCODING_CACHE_TIMEOUT)
        return city_list
    except Exception:
        q = query.strip().lower()
        matched = []
        for key, (lat, lon, display) in DEFAULT_CITIES.items():
            if q in key:
                matched.append({
                    'name': key.title(),
                    'country': 'Default List',
                    'country_code': '',
                    'latitude': lat,
                    'longitude': lon,
                    'timezone': 'UTC',
                    'display_name': display
                })
        return matched


def resolve_city_coordinates(city_name: str) -> Tuple[float, float, str]:
    """
    Resolves city name to latitude, longitude, and display name.
    Tries dynamic geocoding first, falls back to default dictionary.
    """
    normalized = city_name.strip().lower()
    if normalized in DEFAULT_CITIES:
        lat, lon, display = DEFAULT_CITIES[normalized]
        return lat, lon, display

    search_results = search_cities(city_name, count=1)
    if search_results:
        top = search_results[0]
        return top['latitude'], top['longitude'], top['display_name']

    return DEFAULT_CITIES['buenos aires'][0], DEFAULT_CITIES['buenos aires'][1], city_name.title()
