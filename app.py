from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

API_KEY = os.environ.get('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
            }
            return weather_data, None
        else:
            error_msg = response.json().get('message', 'City not found')
            return None, error_msg
            
    except requests.exceptions.RequestException:
        return None, "Unable to connect to weather service"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    """Get weather data for a city"""
    city = request.form.get('city', '').strip()
    
    if not city:
        return jsonify({'error': 'Please enter a city name'})
    
    if not API_KEY:
        return jsonify({'error': 'API key not configured. Please add your OpenWeatherMap API key.'})
    
    weather_data, error = get_weather_data(city)
    
    if error:
        return jsonify({'error': error})
    
    return jsonify({'success': True, 'data': weather_data})

if __name__ == '__main__':
    # Check if API key is set
    if not API_KEY:
        print("\n" + "="*60)
        print("⚠️  IMPORTANT: API KEY REQUIRED")
        print("="*60)
        print("To use this weather app, you need a free API key from OpenWeatherMap:")
        print("1. Go to: https://openweathermap.org/api")
        print("2. Sign up for a free account")
        print("3. Get your API key")
        print("4. Add OPENWEATHER_API_KEY to your environment variables")
        print("="*60 + "\n")
    
    # Production configuration
    import os
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)