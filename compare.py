import tkinter as tk
from tkinter import *
from geopy.geocoders import Nominatim
from datetime import datetime
import requests
from PIL import Image, ImageTk
from timezonefinder import TimezoneFinder
import pytz
from tkinter import messagebox
from plyer import notification

# Function to fetch weather data and update UI
def get_weather():
    try:
        city1 = textfield1.get()
        city2 = textfield2.get()
        
        weather_data_city1 = fetch_weather_data(city1)
        weather_data_city2 = fetch_weather_data(city2)
        
        if weather_data_city1 and weather_data_city2:
            display_weather_data(weather_data_city1, 1)
            display_weather_data(weather_data_city2, 2)
            compare_cities(weather_data_city1, weather_data_city2, city1, city2)
        
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")

# Function to fetch weather data for a city
def fetch_weather_data(city):
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        obj = TimezoneFinder()
        
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        
        # Weather API call
        api_key = "665a28e7b20e491e97063913243107"  # Replace with your WeatherAPI key
        api = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7"
        response = requests.get(api)
        
        if response.status_code == 200:
            json_data = response.json()
            return {
                "city": city,
                "timezone": result,
                "current_time": current_time,
                "latitude": round(location.latitude, 4),
                "longitude": round(location.longitude, 4),
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

# Function to display weather data for a city
def display_weather_data(weather_data, city_number):
    if city_number == 1:
        location_name1.config(text=weather_data["city"])
        timezone_label1.config(text=weather_data["timezone"])
        long_lat_label1.config(text=f"{weather_data['latitude']}°N, {weather_data['longitude']}°E")
        clock1.config(text=weather_data["current_time"])
        temp_label1.config(text=f"{weather_data['temp']} °C")
        humidity_label1.config(text=f"{weather_data['humidity']} %")
        pressure_label1.config(text=f"{weather_data['pressure']} hPa")
        wind_label1.config(text=f"{weather_data['wind']} m/s")
        description_label1.config(text=weather_data["description"])
    else:
        location_name2.config(text=weather_data["city"])
        timezone_label2.config(text=weather_data["timezone"])
        long_lat_label2.config(text=f"{weather_data['latitude']}°N, {weather_data['longitude']}°E")
        clock2.config(text=weather_data["current_time"])
        temp_label2.config(text=f"{weather_data['temp']} °C")
        humidity_label2.config(text=f"{weather_data['humidity']} %")
        pressure_label2.config(text=f"{weather_data['pressure']} hPa")
        wind_label2.config(text=f"{weather_data['wind']} m/s")
        description_label2.config(text=weather_data["description"])

# Function to compare weather data of two cities and display recommendation
def compare_cities(data1, data2, city1, city2):
    if data1["temp"] > data2["temp"]:
        recommendation_label.config(text=f"> Recommendation: Travel to {city2} for cooler weather.", fg="green")
    else:
        recommendation_label.config(text=f"> Recommendation: Travel to {city1} for cooler weather.", fg="green")

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("900x500")
root.configure(bg="#57adff")

# Labels and other GUI elements for City 1
Label(root, text="City 1:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=30, y=30)
location_name1 = Label(root, font=('Helvetica', 14), fg="white", bg="#57adff")
location_name1.place(x=130, y=30)

Label(root, text="Timezone:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=30, y=60)
timezone_label1 = Label(root, font=('Helvetica', 14), fg="white", bg="#57adff")
timezone_label1.place(x=130, y=60)

Label(root, text="Latitude/Longitude:", font=('Helvetica', 10), fg="white", bg="#57adff").place(x=30, y=90)
long_lat_label1 = Label(root, font=('Helvetica', 10), fg="white", bg="#57adff")
long_lat_label1.place(x=160, y=90)

Label(root, text="Local Time:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=30, y=120)
clock1 = Label(root, font=('Helvetica', 14, 'bold'), fg="white", bg="#57adff")
clock1.place(x=130, y=120)

Label(root, text="Current Weather:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=30, y=150)
Label(root, text="Temperature:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=30, y=180)
temp_label1 = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
temp_label1.place(x=140, y=180)

Label(root, text="Humidity:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=30, y=210)
humidity_label1 = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
humidity_label1.place(x=140, y=210)

Label(root, text="Pressure:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=30, y=240)
pressure_label1 = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
pressure_label1.place(x=140, y=240)

Label(root, text="Wind Speed:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=30, y=270)
wind_label1 = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
wind_label1.place(x=140, y=270)

Label(root, text="Description:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=30, y=300)
description_label1 = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
description_label1.place(x=140, y=300)

# Labels and other GUI elements for City 2
Label(root, text="City 2:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=450, y=30)
location_name2 = Label(root, font=('Helvetica', 14), fg="white", bg="#57adff")
location_name2.place(x=550, y=30)

Label(root, text="Timezone:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=450, y=60)
timezone_label2 = Label(root, font=('Helvetica', 14), fg="white", bg="#57adff")
timezone_label2.place(x=550, y=60)

Label(root, text="Latitude/Longitude:", font=('Helvetica', 10), fg="white", bg="#57adff").place(x=450, y=90)
long_lat_label2 = Label(root, font=('Helvetica', 10), fg="white", bg="#57adff")
long_lat_label2.place(x=580, y=90)

Label(root, text="Local Time:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=450, y=120)
clock2 = Label(root, font=('Helvetica', 14, 'bold'), fg="white", bg="#57adff")
clock2.place(x=550, y=120)

Label(root, text="Current Weather:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=450, y=150)
Label(root, text="Temperature:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=450, y=180)
temp_label2 = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
temp_label2.place(x=560, y=180)

Label(root, text="Humidity:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=450, y=210)
humidity_label2 = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
humidity_label2.place(x=560, y=210)

Label(root, text="Pressure:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=450, y=240)
pressure_label2 = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
pressure_label2.place(x=560, y=240)

Label(root, text="Wind Speed:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=450, y=270)
wind_label2 = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
wind_label2.place(x=560, y=270)

Label(root, text="Description:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=450, y=300)
description_label2 = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
description_label2.place(x=560, y=300)

# Text fields for user input
textfield1 = Entry(root, font=('Helvetica', 14), bg="white", width=20)
textfield1.place(x=130, y=30)

textfield2 = Entry(root, font=('Helvetica', 14), bg="white", width=20)
textfield2.place(x=550, y=30)

# Button to fetch weather
search_button = Button(root, text="Compare", font=('Helvetica', 12), relief=RAISED, command=get_weather)
search_button.place(x=400, y=400)

# Recommendation label
recommendation_label = Label(root, font=('Helvetica', 14, 'bold'), fg="green", bg="#57adff")
recommendation_label.place(x=280, y=350)

root.mainloop()
