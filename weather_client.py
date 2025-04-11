import requests
from datetime import datetime

api_key =open('api.txt','r').read()

user_input = input('Name of the place: ')

base_url = "http://api.openweathermap.org/data/2.5/forecast"
complete_url = f"{base_url}?q={user_input}&appid={api_key}"

response = requests.get(complete_url)
json_data = response.json()

# Error handling
if response.status_code != 200 or 'city' not in json_data:
    print("Error fetching forecast. Please check the city name or your API key.")
    exit()

# Get city data
city = json_data['city']
print(f"\nCity: {city['name']}")
print(f"Latitude: {city['coord']['lat']}°, Longitude: {city['coord']['lon']}°")

# Prepare forecast strings
forecast = f"\n[ {city['name']} - 5 Day Forecast ]\n"

# Store forecasts for day and night
daily_forecasts = {}

for item in json_data['list']:
    dt = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
    date_str = dt.date().isoformat()
    time_str = dt.strftime('%H:%M')

    if date_str not in daily_forecasts:
        daily_forecasts[date_str] = {}

    if time_str == "12:00":
        daily_forecasts[date_str]['day'] = item
    elif time_str in ["21:00", "00:00"]:
        daily_forecasts[date_str]['night'] = item

# Function to display forecast details
def format_forecast(label, data):
    temp = int(data['main']['temp'] - 273.15)
    feels_like = int(data['main']['feels_like'] - 273.15)
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description'].title()
    cloudiness = data['clouds']['all']
    wind_speed_mps = data['wind']['speed']
    wind_speed_kmph = round(wind_speed_mps * 3.6, 1)
    wind_deg = data['wind']['deg']
    pop = int(data.get('pop', 0) * 100)

    return (
        f"{label} ({data['dt_txt'][11:16]}):\n"
        f"  Temperature: {temp}°C (Feels like {feels_like}°C)\n"
        f"  Pressure: {pressure} hPa\n"
        f"  Humidity: {humidity}%\n"
        f"  Weather: {description}\n"
        f"  Cloudiness: {cloudiness}%\n"
        f"  Wind: {wind_speed_mps} m/s ({wind_speed_kmph} km/h), {wind_deg}°\n"
        f"  Precipitation Probability (Rain): {pop}%\n"
    )

# Print forecast (limit to 5 days)
count = 0
for date, times in sorted(daily_forecasts.items()):
    if count >= 5:
        break

    forecast += f"\n📅 {datetime.strptime(date, '%Y-%m-%d').strftime('%A, %d %B %Y')}\n"

    if 'day' in times:
        forecast += format_forecast("☀️ Daytime", times['day'])

    if 'night' in times:
        forecast += format_forecast("🌙 Nighttime", times['night'])

    count += 1

print(forecast)