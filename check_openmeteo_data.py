import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,cloud_cover,surface_pressure,wind_direction_10m",
    "timezone": "auto"
}

response = requests.get(url, params=params)

data = response.json()

print(data)
