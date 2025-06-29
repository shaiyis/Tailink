# import googlemaps # type: ignore
from django.conf import settings

def get_place_details(place_name):
    """Fetch place details (address, lat, lng) from Google Maps API"""
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    
    result = gmaps.places(query=place_name)
    
    if not result['results']:
        return None  # No place found

    place = result['results'][0]  # Take the first result
    print(f'place: {place}')
    details = {
        "name": place['name'],
        "address": place['formatted_address'],
        "latitude": place['geometry']['location']['lat'],
        "longitude": place['geometry']['location']['lng']
    }
    
    return details
