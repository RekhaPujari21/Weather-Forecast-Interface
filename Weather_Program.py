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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to fetch weather data and update UI
def get_weather():
    try:
        city = textfield.get()
        
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        obj = TimezoneFinder()
        
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        
        timezone_label.config(text=result)
        long_lat_label.config(text=f"{round(location.latitude, 4)}°N, {round(location.longitude, 4)}°E")
        
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        
        # Weather API call
        api_key = "57a78e1ecefa4a3d9ee134623240407"  # Replace with your WeatherAPI key
        api = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7"
        response = requests.get(api)
        
        if response.status_code == 200:
            json_data = response.json()
            
            # Current weather
            temp = json_data['current']['temp_c']
            humidity = json_data['current']['humidity']
            pressure = json_data['current']['pressure_mb']
            wind = json_data['current']['wind_kph']
            description = json_data['current']['condition']['text']
            temp_label.config(text=f"{temp} °C")
            humidity_label.config(text=f"{humidity} %")
            pressure_label.config(text=f"{pressure} hPa")
            wind_label.config(text=f"{wind} m/s")
            description_label.config(text=description)
            
            # Notify user based on weather conditions
            notify_user(description)
            
            # Day forecasts
            temp_data = []
            for i in range(7):
                day_image = json_data['forecast']['forecastday'][i]['day']['condition']['icon']
                img = Image.open(requests.get(f"http:{day_image}", stream=True).raw).resize((50, 50))
                photo = ImageTk.PhotoImage(img)
                
                if i == 0:
                    first_image.config(image=photo)
                    first_image.image = photo
                    temp_day = json_data['forecast']['forecastday'][0]['day']['maxtemp_c']
                    temp_night = json_data['forecast']['forecastday'][0]['day']['mintemp_c']
                    day1_temp_label.config(text=f"Day: {temp_day}°C\nNight: {temp_night}°C")
                elif i == 1:
                    second_image.config(image=photo)
                    second_image.image = photo
                    temp_day = json_data['forecast']['forecastday'][1]['day']['maxtemp_c']
                    temp_night = json_data['forecast']['forecastday'][1]['day']['mintemp_c']
                    day2_temp_label.config(text=f"Day: {temp_day}°C\nNight: {temp_night}°C")
                elif i == 2:
                    third_image.config(image=photo)
                    third_image.image = photo
                    temp_day = json_data['forecast']['forecastday'][2]['day']['maxtemp_c']
                    temp_night = json_data['forecast']['forecastday'][2]['day']['mintemp_c']
                    day3_temp_label.config(text=f"Day: {temp_day}°C\nNight: {temp_night}°C")
                elif i == 3:
                    fourth_image.config(image=photo)
                    fourth_image.image = photo
                    temp_day = json_data['forecast']['forecastday'][3]['day']['maxtemp_c']
                    temp_night = json_data['forecast']['forecastday'][3]['day']['mintemp_c']
                    day4_temp_label.config(text=f"Day: {temp_day}°C\nNight: {temp_night}°C")
                elif i == 4:
                    fifth_image.config(image=photo)
                    fifth_image.image = photo
                    temp_day = json_data['forecast']['forecastday'][4]['day']['maxtemp_c']
                    temp_night = json_data['forecast']['forecastday'][4]['day']['mintemp_c']
                    day5_temp_label.config(text=f"Day: {temp_day}°C\nNight: {temp_night}°C")
                elif i == 5:
                    sixth_image.config(image=photo)
                    sixth_image.image = photo
                    temp_day = json_data['forecast']['forecastday'][5]['day']['maxtemp_c']
                    temp_night = json_data['forecast']['forecastday'][5]['day']['mintemp_c']
                    day6_temp_label.config(text=f"Day: {temp_day}°C\nNight: {temp_night}°C")
                elif i == 6:
                    seventh_image.config(image=photo)
                    seventh_image.image = photo
                    temp_day = json_data['forecast']['forecastday'][6]['day']['maxtemp_c']
                    temp_night = json_data['forecast']['forecastday'][6]['day']['mintemp_c']
                    day7_temp_label.config(text=f"Day: {temp_day}°C\nNight: {temp_night}°C")
                
                # Collect temperature data for plotting
                temp_data.append((temp_day, temp_night))
                    
            # Live location name
            location_name.config(text=location.address)
            
            # Plot temperature trends
            plot_temperature_trends(temp_data)
        
        else:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            messagebox.showerror("Error", f"Failed to fetch data: {response.status_code} - {error_message}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")

# Function to notify user based on weather conditions
def notify_user(description):
    if "rain" in description.lower():
        notification.notify(title="Weather Alert", message="It's raining!", timeout=50)
    elif "cloudy" in description.lower():
        notification.notify(title="Weather Alert", message="It's cloudy!", timeout=50)
    elif "sunny" in description.lower():
        notification.notify(title="Weather Alert", message="It's sunny!", timeout=50)

# Function to plot temperature trends
def plot_temperature_trends(temp_data):
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    temp_data = np.array(temp_data)
    day_temps = temp_data[:, 0]
    night_temps = temp_data[:, 1]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(days, day_temps, label="Day Temperature", marker='o')
    ax.plot(days, night_temps, label="Night Temperature", marker='o')
    ax.set_xlabel("Days")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("7-Day Temperature Trend")
    ax.legend()
    ax.grid(True)

    # Clear previous plot from plot frame
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Embed plot in plot frame
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("900x700")
root.configure(bg="#57adff")

# Labels and other GUI elements
Label(root, text="Location:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=30, y=90)
location_name = Label(root, font=('Helvetica', 14), fg="white", bg="#57adff")
location_name.place(x=130, y=90)

Label(root, text="Timezone:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=600, y=90)
timezone_label = Label(root, font=('Helvetica', 14), fg="white", bg="#57adff")
timezone_label.place(x=690, y=90)

Label(root, text="Latitude/Longitude:", font=('Helvetica', 10), fg="white", bg="#57adff").place(x=30, y=120)
long_lat_label = Label(root, font=('Helvetica', 10), fg="white", bg="#57adff")
long_lat_label.place(x=160, y=120)

Label(root, text="Local Time:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=600, y=120)
clock = Label(root, font=('Helvetica', 14, 'bold'), fg="white", bg="#57adff")
clock.place(x=710, y=120)

Label(root, text="Current Weather:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=30, y=170)

Label(root, text="Temperature:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=30, y=210)
temp_label = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
temp_label.place(x=140, y=210)

Label(root, text="Humidity:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=30, y=240)
humidity_label = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
humidity_label.place(x=140, y=240)

Label(root, text="Pressure:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=30, y=270)
pressure_label = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
pressure_label.place(x=140, y=270)

Label(root, text="Wind Speed:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=30, y=300)
wind_label = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
wind_label.place(x=140, y=300)

Label(root, text="Description:", font=('Helvetica', 12), fg="white", bg="#57adff").place(x=30, y=330)
description_label = Label(root, font=('Helvetica', 12), fg="white", bg="#57adff")
description_label.place(x=140, y=330)

Label(root, text="Weather Forecast:", font=('Helvetica', 14), fg="white", bg="#57adff").place(x=30, y=400)

first_image = Label(root, bg="#57adff")
first_image.place(x=30, y=450)
day1_temp_label = Label(root, font=('Helvetica', 10), fg="white", bg="#57adff")
day1_temp_label.place(x=90, y=450)

second_image = Label(root, bg="#57adff")
second_image.place(x=30, y=510)
day2_temp_label = Label(root, font=('Helvetica', 10), fg="white", bg="#57adff")
day2_temp_label.place(x=90, y=510)

third_image = Label(root, bg="#57adff")
third_image.place(x=30, y=570)
day3_temp_label = Label(root, font=('Helvetica', 10), fg="white", bg="#57adff")
day3_temp_label.place(x=90, y=570)

fourth_image = Label(root, bg="#57adff")
fourth_image.place(x=30, y=630)
day4_temp_label = Label(root, font=('Helvetica', 10), fg="white", bg="#57adff")
day4_temp_label.place(x=90, y=630)

fifth_image = Label(root, bg="#57adff")
fifth_image.place(x=240, y=450)
day5_temp_label = Label(root, font=('Helvetica', 10), fg="white", bg="#57adff")
day5_temp_label.place(x=300, y=450)

sixth_image = Label(root, bg="#57adff")
sixth_image.place(x=240, y=510)
day6_temp_label = Label(root, font=('Helvetica', 10), fg="white", bg="#57adff")
day6_temp_label.place(x=300, y=510)

seventh_image = Label(root, bg="#57adff")
seventh_image.place(x=240, y=570)
day7_temp_label = Label(root, font=('Helvetica', 10), fg="white", bg="#57adff")
day7_temp_label.place(x=300, y=570)

# Plot frame setup
plot_frame = Frame(root, bg="#57adff", width=800, height=300)
plot_frame.place(x=550, y=350)

# Text field for user input
textfield = Entry(root, font=('Helvetica', 14), bg="white", width=20)
textfield.place(x=130, y=90)

# Button to fetch weather
search_button = Button(root, text="Search", font=('Helvetica', 12), relief=RAISED, command=get_weather)
search_button.place(x=330, y=87)

root.mainloop()
