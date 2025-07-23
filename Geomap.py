import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests
from timezonefinder import TimezoneFinder
import pytz
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Function to fetch weather data using latitude and longitude
def fetch_weather_data(lat, lon):
    try:
        obj = TimezoneFinder()
        timezone_str = obj.timezone_at(lng=lon, lat=lat)
        
        home = pytz.timezone(timezone_str)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        
        # Weather API call
        api_key = "d3355dd286364ab79ad04555242707"  # Replace with your WeatherAPI key
        api = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={lat},{lon}&days=7"
        response = requests.get(api)
        
        if response.status_code == 200:
            json_data = response.json()
            location = json_data['location']['name']
            return {
                "location": location,
                "timezone": timezone_str,
                "current_time": current_time,
                "latitude": round(lat, 4),
                "longitude": round(lon, 4),
                "temp": json_data['current']['temp_c'],
                "humidity": json_data['current']['humidity'],
                "pressure": json_data['current']['pressure_mb'],
                "wind": json_data['current']['wind_kph'],
                "description": json_data['current']['condition']['text']
            }
        else:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            messagebox.showerror("Error", f"Failed to fetch data: {response.status_code} - {error_message}")
            return None
    
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")
        return None

# Function to show the world map and allow user to click for weather data
def show_map():
    fig = plt.figure(figsize=(10, 6))
    m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90,
                llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m.drawcoastlines()
    m.drawcountries()
    
    def on_click(event):
        if event.xdata is not None and event.ydata is not None:
            # Conversion from map projection coordinates to lat/lon
            lon, lat = m(event.xdata, event.ydata, inverse=True)
            # Ensure that lat and lon are within valid ranges
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                weather_data = fetch_weather_data(lat, lon)
                if weather_data:
                    messagebox.showinfo("Weather Info", f"Location: {weather_data['location']}\n"
                                                        f"Weather: {weather_data['description']}\n"
                                                        f"Temperature: {weather_data['temp']}°C\n"
                                                        f"Humidity: {weather_data['humidity']}%\n"
                                                        f"Pressure: {weather_data['pressure']} hPa\n"
                                                        f"Wind Speed: {weather_data['wind']} m/s\n"
                                                        f"Local Time: {weather_data['current_time']}\n"
                                                        f"Timezone: {weather_data['timezone']}\n"
                                                        f"Coordinates: {weather_data['latitude']}°N, {weather_data['longitude']}°E")
            else:
                messagebox.showerror("Error", "Clicked coordinates are out of range.")
    
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()

# Show the world map directly
show_map()
