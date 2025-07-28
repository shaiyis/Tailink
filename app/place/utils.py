import requests
from django.conf import settings

def get_place_details_tomtom(place_name):
    """Fetch place details (address, lat, lng) from TOMTOM Maps API"""
    url = "https://api.tomtom.com/search/2/geocode/" + requests.utils.quote(place_name) + ".json"
    params = {
        "key": settings.TOMTOM_MAPS_API_KEY,
        "language": "he-IL",
        "view": "IL",
        "countrySet": "IL",
        "limit": 1
    }
    
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        return None  # Handle error appropriately in production
    data = resp.json()
    if data.get("summary", {}).get("numResults", 0) < 1:
        return None

    r = data['results'][0]
    addr = r['address']
    print(addr)
    name = addr.get("freeformAddress")
    if not name:
        parts = [addr.get("streetName"), addr.get("municipality"), addr.get("country")]
        name = ", ".join(filter(None, parts))

    return {
        "name": name,
        "address": addr.get("freeformAddress", ""),
        "latitude": r['position']['lat'],
        "longitude": r['position']['lon'],
    }
