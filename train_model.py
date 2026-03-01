import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# ---- STEP 1: Create training data ----
# Since we only have current data from API, we'll generate
# realistic historical data to train our model on
np.random.seed(42)
days = 365

data = {
    "pm25": np.random.normal(60, 20, days).clip(10, 200),
    "pm10": np.random.normal(80, 25, days).clip(15, 250),
    "temperature": np.random.normal(28, 8, days).clip(5, 45),
    "humidity": np.random.normal(55, 15, days).clip(10, 95),
    "wind": np.random.normal(3, 1.5, days).clip(0, 15),
    "day_of_year": np.arange(1, days + 1)
}

# AQI is calculated from these factors realistically
data["aqi"] = (
    data["pm25"] * 1.2 +
    data["pm10"] * 0.5 +
    data["humidity"] * 0.3 -
    data["wind"] * 2 +
    np.random.normal(0, 10, days)
).clip(0, 500)

df = pd.DataFrame(data)
print("Training data created!")
print(df.head())
print(f"\nData shape: {df.shape}")

# ---- STEP 2: Prepare features and target ----
features = ["pm25", "pm10", "temperature", "humidity", "wind", "day_of_year"]
target = "aqi"

X = df[features]
y = df[target]

# ---- STEP 3: Split into train and test sets ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# ---- STEP 4: Train the model ----
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("\nModel trained successfully! ✅")

# ---- STEP 5: Evaluate the model ----
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nModel Performance:")
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R2 Score: {r2:.2f}")

# ---- STEP 6: Plot feature importance ----
importance = model.feature_importances_
feat_df = pd.DataFrame({
    "feature": features,
    "importance": importance
}).sort_values("importance", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=feat_df, x="importance", y="feature", palette="Reds_r")
plt.title("Which factors affect AQI the most?")
plt.xlabel("Importance Score")
plt.ylabel("Factor")
plt.tight_layout()
plt.savefig("outputs/feature_importance.png")
plt.show()
print("Feature importance graph saved! ✅")

# ---- STEP 7: Plot actual vs predicted ----
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5, color="red")
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()], "b--", lw=2)
plt.xlabel("Actual AQI")
plt.ylabel("Predicted AQI")
plt.title("Actual vs Predicted AQI")
plt.tight_layout()
plt.savefig("outputs/actual_vs_predicted.png")
plt.show()
print("Actual vs Predicted graph saved! ✅")

# ---- STEP 8: Save the trained model ----
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/aqi_model.pkl")
print("\nModel saved to models/aqi_model.pkl ✅")
