import pytest
from unittest.mock import patch, Mock
from weather_client import WeatherForecast  # Call the WeatherForecast class from the weather_client script

# A sample fake response for successful forecast data
fake_data = {
    "city": {
        "name": "Ibadan",
        "coord": {"lat": 7.38, "lon": 3.93}
    },
    "list": [
        {
            "dt_txt": "2025-04-11 12:00:00",
            "main": {
                "temp": 300.15,
                "feels_like": 299.15,
                "pressure": 1010,
                "humidity": 70
            },
            "weather": [{"description": "light rain"}],
            "clouds": {"all": 75},
            "wind": {"speed": 3.5, "deg": 160},
            "pop": 0.5
        },
        {
            "dt_txt": "2025-04-11 21:00:00",
            "main": {
                "temp": 295.15,
                "feels_like": 294.15,
                "pressure": 1008,
                "humidity": 80
            },
            "weather": [{"description": "scattered clouds"}],
            "clouds": {"all": 40},
            "wind": {"speed": 2.0, "deg": 150},
            "pop": 0.2
        }
    ]
}

# Create a weather app instance with a fake API key
@pytest.fixture
def weather():
    return WeatherForecast(api_key="fake_api_key")


# Test for a successful API fetch (mocking the request)
def test_fetch_data_success(weather):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = fake_data
        mock_get.return_value = mock_response

        result = weather.fetch_data("Ibadan")
        assert result['city']['name'] == "Ibadan"
        assert len(result['list']) == 2


# Test for handling different error codes (like 404 Not Found, 401 Unauthorized, etc.)
@pytest.mark.parametrize("status_code, expected_text", [
    (400, "Bad request"),
    (401, "Invalid API key"),
    (402, "Payment required"),
    (403, "Access forbidden"),
    (404, "City 'TestCity' not found")
])
def test_error_responses(weather, capsys, status_code, expected_text):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_get.return_value = mock_response

        result = weather.fetch_data("TestCity")

        captured = capsys.readouterr()  # This captures printed output
        assert expected_text in captured.out
        assert result is None


# Test the formatting function to make sure it includes important info
def test_format_forecast(weather):
    item = fake_data['list'][0]
    forecast = weather.format_forecast("☀️ Daytime", item)

    assert "Temperature" in forecast
    assert "Pressure" in forecast
    assert "Humidity" in forecast
    assert "Wind" in forecast
    assert "Precipitation" in forecast


# Test the main forecast parser to make sure it prints the expected sections
def test_parse_forecast_prints(weather, capsys):
    weather.parse_forecast(fake_data)

    output = capsys.readouterr().out
    assert "City: Ibadan" in output
    assert "5 Day Forecast" in output
    assert "Daytime" in output or "Nighttime" in output