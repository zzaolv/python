import requests
#from main import cache
#@cache.cached(timeout=60 * 60)  # 缓存一个小时 (60 * 60 秒)
from cache_config import cache

@cache.cached(timeout=60 * 60)  # 缓存一个小时 (60 * 60 秒)

def get_ip_info():
    api_key = 'b5c8bde6f6899b30c8e83d7193653367'
    url = f"http://restapi.amap.com/v3/ip?key={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_weather(city, api_key):
    url = f"http://restapi.amap.com/v3/weather/weatherInfo?key={api_key}&city={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data['lives']:
            weather_info = data['lives'][0]
            weather = {
                'city': weather_info['city'],
                'description': weather_info['weather'],
                'temperature': weather_info['temperature'],
                'humidity': weather_info['humidity'],
                'wind_speed': weather_info['windpower']
            }
            return weather
        else:
            return None
    else:
        return None
