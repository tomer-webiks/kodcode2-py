import requests
import math
from datetime import datetime, timedelta


def get_weather(city):
    api_key = "9e937ddc46bd06921d4877ed44b75fdf"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        # Calculate tomorrow's date at midnight
        tomorrow_midnight = (datetime.utcnow() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_midnight_str = tomorrow_midnight.strftime('%Y-%m-%d %H:%M:%S')
        
        # Find the forecast for tomorrow at midnight
        for forecast in data['list']:
            if forecast['dt_txt'] == tomorrow_midnight_str:
                weather = forecast['weather'][0]['main']
                wind_speed = forecast['wind']['speed']
                cloudiness = forecast['clouds']['all']
                return weather, wind_speed, cloudiness
        
        # If no forecast is found for tomorrow at midnight
        print("No forecast data available for tomorrow at midnight.")
        return None, None, None
    except Exception as e:
        print(f"Error fetching weather data: {e}\nReturning null values")
        return null, null, null  # Default to Clear if API call fails


def get_lat_lon(city):
    api_key = "9e937ddc46bd06921d4877ed44b75fdf"
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "Clear"  # Default to Clear if API call fails


# Function to calculate the distance between two coordinates using the Haversine formula
def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371.0  # Radius of the Earth in kilometers

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate differences between the coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = r * c
    return distance


# Run the simulation
if __name__ == "__main__":
    # Example usage: Calculate the distance between Tel Aviv and Haifa
    coords_1 = get_lat_lon('haifa')  # Latitude, Longitude of Tel Aviv
    coords_2 = get_lat_lon('teheran')  # Latitude, Longitude of Haifa

    distance = haversine_distance(coords_1[0], coords_1[0], coords_2[1], coords_2[1])
    print(f"Distance between Tel Aviv and Haifa: {distance:.2f} km")