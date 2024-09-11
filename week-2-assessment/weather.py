import requests

def get_weather(city):
    api_key = "9e937ddc46bd06921d4877ed44b75fdf"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        weather = data['weather'][0]['main']
        return weather
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "Clear"  # Default to Clear if API call fails
