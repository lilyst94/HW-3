# Your API KEYS (you need to use your own keys - very long random characters)
import json
import urllib.request
import requests
from urllib.error import URLError, HTTPError
from config import MAPBOX_TOKEN, MBTA_API_KEY, WEATHER_API

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# A little bit of scaffolding if you want to use it
def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.
    Both get_lat_long() and get_nearest_station() might need to use this function.
    """
    try:
        with urllib.request.urlopen(url) as f:
            response = f.read().decode('utf-8')
            response_data = json.loads(response)
            return response_data
    except (HTTPError, URLError) as e:
        print(f"Error getting data from {url}: {e}")
        return{}
    

def get_lat_long(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
   
    place_name = place_name.replace(" ", "%20")
    url = f'{MAPBOX_BASE_URL}/{place_name}.json?access_token={MAPBOX_TOKEN}&types=poi'
    response_data = get_json(url)
    longitude, latitude = response_data["features"][0]["center"]
    return latitude, longitude

def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = f"{MBTA_BASE_URL}?filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance&api_key={MBTA_API_KEY}"
    response_data = get_json(url)

    station_name = response_data["data"][0]["attributes"]["name"]
    wheelchair_accessibility = response_data["data"][0]["attributes"]["wheelchair_boarding"]

    return station_name, wheelchair_accessibility

# def find_stop_near(place_name: str) -> str:
def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    This function might use all the functions above.
    """
    longitude, latitude = get_lat_long(place_name)
    name, accessible = get_nearest_station(longitude, latitude)

    if accessible == 0:
        wheelchair_message = "This is no information about wheelchair accessibility."
    elif accessible == 1:
        wheelchair_message = "This stop is wheelchair accessible."
    elif accessible == 2:
        wheelchair_message = "This stop is not wheelchair accessible."
    
    result = f"The nearest MBTA stop is {name}. {wheelchair_message}"
    return result, accessible

def get_weather(place_name):
    """
    Returns weather in Farenheit for Boston, MA
    """
    city = "Boston"
    country_code = 'us'

    place_name = place_name.replace(" ", "%20")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&APPID={WEATHER_API}&units=imperial"
    response_data = get_json(url)
    
    temp = response_data["main"]["temp"]
    desc = response_data["weather"][0]["description"]

    return {"large": f"{temp}°F", "small": f"Weather: {desc}"}



def main():
    """
    You should test all the above functions here
    """
    place_name = input("Current Location: ")
    print(find_stop_near(place_name))
    print(get_weather(place_name))
if __name__ == '__main__':
    main()
