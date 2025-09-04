from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# OpenWeatherMap API configuration
API_KEY = os.environ.get('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        city = request.form.get('city')
        if not city:
            return jsonify({'error': 'City name is required'})
        
        # Make API request to OpenWeatherMap
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 404:
            return jsonify({'error': 'City not found. Please check the spelling and try again.'})
        elif response.status_code != 200:
            return jsonify({'error': 'Unable to fetch weather data. Please try again later.'})
        
        data = response.json()
        
        # Format the weather data
        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': round(data['wind']['speed'], 1),
            'visibility': round(data['visibility'] / 1000, 1),
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        }
        
        return jsonify({'data': weather_data})
        
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching weather data.'})

@app.route('/weather/location', methods=['POST'])
def get_weather_by_location():
    try:
        lat = request.form.get('lat')
        lon = request.form.get('lon')
        
        if not lat or not lon:
            return jsonify({'error': 'Location coordinates are required'})
        
        # Make API request to OpenWeatherMap using coordinates
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code != 200:
            return jsonify({'error': 'Unable to fetch weather data for your location.'})
        
        data = response.json()
        
        # Format the weather data
        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': round(data['wind']['speed'], 1),
            'visibility': round(data['visibility'] / 1000, 1),
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        }
        
        return jsonify({'data': weather_data})
        
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching weather data.'})

if __name__ == '__main__':
    app.run(debug=True)
