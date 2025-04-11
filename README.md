# 🌦️ Weather Forecast API

An interactive Python script that fetches a 5-day weather forecast for any city using the OpenWeatherMap API.

## 🚀 Features
- Day + night forecast for 5 days
- Temp, humidity, wind, pressure, rain chance
- Error handling (400–404)
- Interactive: enter multiple cities
- Tested with `pytest`

## 📦 Requirements
- Python 3.7+
- `requests`
- `datetime`
- `pytest` (for testing)

Install with:

```bash
pip install requests pytest
```

## ▶️ Run
```bash
python weather_client.py
```

Type `exit` to stop.

## 🧪 Test
```bash
pytest test_weather_client.py -v
```

## 🔑 API Key
1. Get one at [openweathermap.org](https://openweathermap.org)
2. Paste it in the script as `api_key = "your_key"`

## 📁 Files
- `weather_client.py` – main app
- `test_weather_client.py` – tests
- `README.md` – this doc

---

Made by Chidimma Ijoma
