import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("AQI_API_KEY")

def fetch_aqi_data(city):
    url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    if data["status"] != "ok":
        print(f"Error fetching data for {city}")
        return None
    
    aqi_info = data["data"]
    
    result = {
        "city": city,
        "aqi": aqi_info["aqi"],
        "pm25": aqi_info["iaqi"].get("pm25", {}).get("v", None),
        "pm10": aqi_info["iaqi"].get("pm10", {}).get("v", None),
        "temperature": aqi_info["iaqi"].get("t", {}).get("v", None),
        "humidity": aqi_info["iaqi"].get("h", {}).get("v", None),
        "wind": aqi_info["iaqi"].get("w", {}).get("v", None),
        "time": aqi_info["time"]["s"]
    }
    
    return result

def check_alert(aqi):
    if aqi <= 50:
        return "Good ✅"
    elif aqi <= 100:
        return "Moderate ⚠️"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups 🟠"
    elif aqi <= 200:
        return "Unhealthy 🔴"
    elif aqi <= 300:
        return "Very Unhealthy ☠️"
    else:
        return "Hazardous ☢️"

# Test it
if __name__ == "__main__":
    cities = ["delhi", "mumbai", "bangalore", "jaipur"]
    
    results = []
    for city in cities:
        data = fetch_aqi_data(city)
        if data:
            data["alert"] = check_alert(data["aqi"])
            results.append(data)
            print(f"{city.upper()} → AQI: {data['aqi']} | {data['alert']}")
    
    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv("data/aqi_data.csv", index=False)
    print("\nData saved to data/aqi_data.csv ✅")
