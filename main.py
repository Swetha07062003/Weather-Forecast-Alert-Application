import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Alert Thresholds
HIGH_TEMP_THRESHOLD = 35
HIGH_HUMIDITY_THRESHOLD = 85
HIGH_WIND_THRESHOLD = 10

city = input("Enter city name: ")

params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
}

try:
    response = requests.get(BASE_URL, params=params)

    data = response.json()

    if response.status_code != 200:
        print("\nError:", data.get("message"))

    else:

        city_name = data["name"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        print("\n===== WEATHER REPORT =====")

        print(f"City: {city_name}")
        print(f"Temperature: {temperature} °C")
        print(f"Humidity: {humidity} %")
        print(f"Weather: {weather}")
        print(f"Wind Speed: {wind_speed} m/s")

        # Alert Logic
        alerts = []

        if temperature >= HIGH_TEMP_THRESHOLD:
            alerts.append("High Temperature Alert")

        if humidity >= HIGH_HUMIDITY_THRESHOLD:
            alerts.append("High Humidity Alert")

        if wind_speed >= HIGH_WIND_THRESHOLD:
            alerts.append("High Wind Alert")

        if "rain" in weather.lower():
            alerts.append("Rain Alert")

        print("\n===== ALERT STATUS =====")

        if alerts:
            for alert in alerts:
                print(f"⚠ {alert}")
        else:
            print("No weather alerts")

        # Create weather data dictionary
        weather_data = {
            "Temperature": [temperature],
            "Humidity": [humidity],
            "Wind Speed": [wind_speed]
        }

        # Convert to DataFrame
        df = pd.DataFrame(weather_data)

        # Create folders automatically
        os.makedirs("outputs", exist_ok=True)
        os.makedirs("images", exist_ok=True)

        # Save CSV
        csv_path = f"outputs/{city_name}_weather_report.csv"
        df.to_csv(csv_path, index=False)

        print("\nWeather report saved successfully!")
        print("CSV File:", csv_path)

        # Create Weather Visualization Chart
        plt.figure(figsize=(8, 5))

        categories = ["Temperature", "Humidity", "Wind Speed"]
        values = [temperature, humidity, wind_speed]

        plt.bar(categories, values)

        plt.title(f"Weather Report for {city_name}")
        plt.ylabel("Values")

        # Save chart
        image_path = f"images/{city_name}_weather_chart.png"

        plt.savefig(image_path)

        print("Chart saved successfully!")
        print("Chart Location:", image_path)

        plt.close()

except Exception as e:
    print("Error:", e)