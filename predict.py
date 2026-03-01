import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from fetch_data import fetch_aqi_data, check_alert

# ---- STEP 1: Load the saved model ----
model = joblib.load("models/aqi_model.pkl")
print("Model loaded successfully! ✅")

# ---- STEP 2: Fetch real current data ----
cities = ["delhi", "mumbai", "bangalore", "jaipur"]

print("\n📡 Fetching real-time AQI data...\n")
current_data = []

for city in cities:
    data = fetch_aqi_data(city)
    if data:
        current_data.append(data)

df_current = pd.DataFrame(current_data)
print(df_current[["city", "aqi", "pm25", "pm10", "temperature", "humidity"]])

# ---- STEP 3: Predict future AQI for next 7 days ----
print("\n🔮 Predicting AQI for next 7 days...\n")

predictions = []

for _, row in df_current.iterrows():
    city = row["city"]
    
    for day in range(1, 8):
        # Simulate slight daily changes realistically
        future = {
            "pm25": max(10, row["pm25"] + np.random.normal(0, 5)) if row["pm25"] else 60,
            "pm10": max(15, row["pm10"] + np.random.normal(0, 7)) if row["pm10"] else 80,
            "temperature": row["temperature"] + np.random.normal(0, 2) if row["temperature"] else 28,
            "humidity": min(95, max(10, row["humidity"] + np.random.normal(0, 3))) if row["humidity"] else 55,
            "wind": max(0, row["wind"] + np.random.normal(0, 0.5)) if row["wind"] else 3,
            "day_of_year": (pd.Timestamp.now().day_of_year + day) % 365
        }

        predicted_aqi = model.predict(pd.DataFrame([future]))[0]
        alert = check_alert(predicted_aqi)

        predictions.append({
            "city": city,
            "day": f"Day {day}",
            "predicted_aqi": round(predicted_aqi, 1),
            "alert": alert
        })

df_predictions = pd.DataFrame(predictions)

# ---- STEP 4: Print predictions with alerts ----
print(f"{'City':<12} {'Day':<8} {'Predicted AQI':<15} {'Alert'}")
print("-" * 55)
for _, row in df_predictions.iterrows():
    print(f"{row['city']:<12} {row['day']:<8} {row['predicted_aqi']:<15} {row['alert']}")

# ---- STEP 5: Plot predictions ----
plt.figure(figsize=(14, 7))

for city in cities:
    city_data = df_predictions[df_predictions["city"] == city]
    plt.plot(city_data["day"], city_data["predicted_aqi"],
             marker="o", linewidth=2, label=city.capitalize())

# Add danger zone lines
plt.axhline(y=100, color="orange", linestyle="--", alpha=0.7, label="Moderate threshold")
plt.axhline(y=200, color="red", linestyle="--", alpha=0.7, label="Unhealthy threshold")

plt.title("7-Day AQI Forecast for Indian Cities", fontsize=15)
plt.xlabel("Day")
plt.ylabel("Predicted AQI")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/7day_forecast.png")
plt.show()
print("\n7-day forecast graph saved! ✅")

# ---- STEP 6: Save predictions to CSV ----
df_predictions.to_csv("outputs/predictions_report.csv", index=False)
print("Predictions saved to outputs/predictions_report.csv ✅")

# ---- STEP 7: Print final health alerts ----
print("\n🚨 HEALTH ALERTS 🚨")
print("-" * 40)
for city in cities:
    city_preds = df_predictions[df_predictions["city"] == city]
    avg_aqi = city_preds["predicted_aqi"].mean()
    alert = check_alert(avg_aqi)
    print(f"{city.upper():<12} → Avg 7-day AQI: {avg_aqi:.1f} | {alert}")