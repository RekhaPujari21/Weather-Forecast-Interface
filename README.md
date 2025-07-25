# 🌦️ Weather Forecast Interface Project

This project is a **Tkinter-based Python desktop application** that provides real-time weather information using the **WeatherAPI** and interactive maps with **Basemap**. It includes three major modules:

1. **Live Weather Forecast for a City**  
2. **Compare Weather Between Two Cities**  
3. **Click on Geo Map to Fetch Location Weather**

---

## 🚀 Features

### 1. 🔍 Single City Weather Forecast
- Fetches and displays:
  - Current temperature, humidity, wind speed, pressure, and weather description
  - Latitude, longitude, timezone, and local time
- Displays **7-day forecast** with day & night temperature trends
- Notifies user using **desktop notifications** for weather conditions like rain/clouds/sun
- Shows a **temperature trend graph** using `matplotlib`

### 2. 🌇 Compare Two Cities
- Takes input for two cities
- Displays:
  - Weather data for both cities side by side
  - Location coordinates, local time, temperature, humidity, pressure, and wind speed
- Suggests which city has **cooler weather**
  
### 3. 🌍 Geo Map Location Weather (Basemap)
- Interactive world map
- User can **click anywhere on the map** to fetch weather data of that location
- Shows:
  - Local time, timezone
  - Coordinates
  - Weather details (temperature, humidity, pressure, wind speed, condition)
  - Displayed in a `messagebox` popup

---

## 🧰 Technologies Used

- **Python 3**
- **Tkinter** - GUI toolkit
- **Pillow (PIL)** - Image handling
- **Matplotlib** - Graphs and visualizations
- **Basemap** - World map interaction
- **Geopy** - Location and geocoding
- **TimezoneFinder** - Get timezone using lat/lon
- **Pytz** - Timezone conversion
- **Requests** - HTTP API calls
- **Plyer** - Desktop notifications

---

## 📦 Requirements

Install the following dependencies before running:

```
pip install tkinter
pip install geopy
pip install requests
pip install pillow
pip install timezonefinder
pip install pytz
pip install plyer
pip install matplotlib
pip install basemap
-------------
🔑 Weather API Key
You need a free API key from WeatherAPI.com.

Replace the placeholder key in the code:

api_key = "your_actual_api_key_here"
--------------------------
## Learning Outcome
- Using APIs to fetch live data

- Working with timezones and locations

- Building rich GUI apps using Python

- Implementing data visualizations (matplotlib)

- Interactive user experience with maps
