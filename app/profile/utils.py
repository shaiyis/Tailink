import requests

def get_current_location():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    lat, lon = map(float, data["loc"].split(","))

    return {"latitude": lat, "longitude": lon}
