import requests
from datetime import datetime

api_key =open('api.txt','r').read()

user_input = input('Name of the place: ')

base_url = "http://api.openweathermap.org/data/2.5/forecast"
complete_url = base_url + "?q=" + user_input + "&appid=" + api_key 
#print(complete_url)


json_data = requests.get(complete_url).json()
#print(json_data)


name_of_the_city = json_data['city']['name']
print(name_of_the_city)
city_lat = json_data['city']['coord']['lat']
city_lon = json_data['city']['coord']['lon']
print("latitude : " + str(city_lat) + ", Longitude : " + str(city_lon))

#Let's now format the output to make it readable
string = f'[ {name_of_the_city} - 5 days forecast]\n'


for item in json_data['list']:
    time_forecasted = item['dt_txt']
    time_forecasted = datetime.strptime(time_forecasted, '%Y-%m-%d %H:%M:%S')
    day_forcasted = datetime.strftime(time_forecasted,'%A')
    print("\n" + str(day_forcasted)+ " " + str(time_forecasted))
    temp = str(int(item['main']['temp']-273.15))
    print("Temperature in Celsius: " + temp)
    feels_like = str(int(item['main']['feels_like'] - 273.15))
    print("Temperature in Celsius feels like: " + feels_like)
    pressure = str(item['main']['pressure'])
    print("Atmospheric pressure on sea level in hPa: " + pressure)
    humidity = str(item['main']['humidity'])
    print("Humidity: "+ humidity + "%")
    weather_des = item['weather'][0]['description']
    print("Weather description: "+ weather_des.title())
    cloudiness = str(item['clouds']['all'])
    print("Cloudiness: " + cloudiness + "%")
    windSpd = str(item['wind']['speed'])
    print("Wind speed: \n\t in meter per second is " + windSpd)
    windSpd = str(float(item['wind']['speed']*3600/1000))
    print("\t in kilometer per second is " + windSpd)
    wind_degree = str(item['wind']['deg'])
    print("Wind degree: " + wind_degree + "°")
    pop = str(int(item['pop']*100))
    print("Probability of Precipitation (Rain): " + pop + "%") 