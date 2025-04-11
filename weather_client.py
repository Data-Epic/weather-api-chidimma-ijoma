import requests
from datetime import datetime

class WeatherForecast:
    """
    A class to fetch and display 5-day weather forecasts (day & night) 
    for a given city using the OpenWeatherMap API.
    """
    
    def __init__(self, api_key):
        """
        Initialize with an API key from OpenWeatherMap.
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def fetch_data(self, city):
        """
        Fetch weather data for a given city.
        
        Parameters:
            city (str): The name of the city to fetch weather for.

        Returns:
            dict or None: JSON response as dictionary if successful, None otherwise.
        """
        complete_url = f"{self.base_url}?q={city}&appid={self.api_key}"
        response = requests.get(complete_url)

        # --- Handle common HTTP errors ---
        if response.status_code == 400:
            print("❌ Error 400: Bad request. Check your input or parameters.")
            return None
        elif response.status_code == 401:
            print("❌ Error 401: Unauthorized. Invalid API key.")
            return None
        elif response.status_code == 402:
            print("❌ Error 402: Payment required. Check your OpenWeather subscription plan.")
            return None
        elif response.status_code == 403:
            print("❌ Error 403: Access forbidden. You don't have permission to access this resource.")
            return None
        elif response.status_code == 404:
            print(f"❌ Error 404: City '{city}' not found. Please check the spelling.")
            return None
        elif response.status_code != 200:
            print(f"❌ Unexpected error: {response.status_code}")
            return None

        return response.json()

    def parse_forecast(self, json_data):
        """
        Parse the JSON forecast data and display formatted weather information.

        Parameters:
            json_data (dict): The JSON response from the API.
        """
        city = json_data['city']
        name = city['name']
        lat = city['coord']['lat']
        lon = city['coord']['lon']

        print(f"\n📍 City: {name}") # Display City name
        print(f"🌍 Latitude: {lat}°, Longitude: {lon}°") # Display longititude and latitude

        forecast = f"\n[ {name} - 5 Day Forecast ]\n"
        daily_forecasts = {}

        # Group data by date and filter to include only daytime (12:00) and nighttime (21:00/00:00)
        for item in json_data['list']:
            dt = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
            date_str = dt.date().isoformat()
            time_str = dt.strftime('%H:%M')

            if date_str not in daily_forecasts:
                daily_forecasts[date_str] = {}

            if time_str == "12:00": # Select only the weather data at 12:00
                daily_forecasts[date_str]['day'] = item
            elif time_str in ["21:00", "00:00"]: # Select only the weather data at 21:00 or 00:00
                daily_forecasts[date_str]['night'] = item

        # Display up to 5 days of forecasts
        count = 0
        for date, times in sorted(daily_forecasts.items()):
            if count >= 5:
                break

            forecast += f"\n📅 {datetime.strptime(date, '%Y-%m-%d').strftime('%A, %d %B %Y')}\n"

            if 'day' in times:
                forecast += self.format_forecast("☀️ Daytime", times['day'])
            if 'night' in times:
                forecast += self.format_forecast("🌙 Nighttime", times['night'])

            count += 1

        print(forecast)

    def format_forecast(self, label, data):
        """
        Format the forecast data for display.

        Parameters:
            label (str): Label for the forecast time ("Daytime" or "Nighttime").
            data (dict): The forecast data for the time slot.

        Returns:
            str: A nicely formatted weather summary.
        """
        temp = int(data['main']['temp'] - 273.15) # Convert temperature from Kelvin to Celsius
        feels_like = int(data['main']['feels_like'] - 273.15) # Convert temperature from Kelvin to Celsius
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
            f"  Temperature🌡 : {temp}°C (Feels like {feels_like}°C)\n"
            f"  Pressure🎚️ : {pressure} hPa\n"
            f"  Humidity💧 : {humidity}%\n"
            f"  Weather🌈 : {description}\n"
            f"  Cloudiness☁ : {cloudiness}%\n"
            f"  Wind💨 : {wind_speed_mps} m/s ({wind_speed_kmph} km/h), {wind_deg}°\n"
            f"  Precipitation Probability🌧 : {pop}%\n\n"
        )


# --- Main Script Execution ---
if __name__ == "__main__":
    """
    Run the interactive script to accept city names and display weather forecasts.
    """
    api_key = open('api.txt','r').read()
    weather_app = WeatherForecast(api_key)

    print("🌦️   Multi-Location Weather Forecast App")
    print("Type 'exit' to stop.\n")

    while True:
        city_name = input("Enter city name: ").strip()
        if city_name.lower() == 'exit':
            print("👋 Goodbye!")
            break

        data = weather_app.fetch_data(city_name)
        if data:
            weather_app.parse_forecast(data)