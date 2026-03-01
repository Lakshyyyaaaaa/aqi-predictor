# 🌫️ AQI Predictor — Air Quality Forecasting with Machine Learning

A machine learning project that fetches **real-time air quality data** from Indian cities, predicts **future AQI levels for the next 7 days**, and generates **health alerts** based on WHO standards.

---

## 🚀 Features

- 📡 **Real-time AQI data** fetched live from WAQI API (Delhi, Mumbai, Bangalore, Jaipur)
- 🤖 **ML model** trained using Random Forest to predict future pollution levels
- 📈 **7-day AQI forecast** with visual graphs
- 🚨 **Health alerts** based on official EPA/WHO air quality standards
- 📊 **Data visualizations** — feature importance, actual vs predicted, forecast chart
- 💾 **CSV report** of all predictions saved automatically

---

## 🛠️ Tech Stack

| Library                  | Purpose                          |
| ------------------------ | -------------------------------- |
| `pandas`                 | Data handling and CSV operations |
| `numpy`                  | Numerical calculations           |
| `scikit-learn`           | Random Forest ML model           |
| `matplotlib` & `seaborn` | Data visualization               |
| `requests`               | Fetching real-time API data      |
| `python-dotenv`          | Secure API key management        |
| `joblib`                 | Saving and loading trained model |

---

## 📁 Project Structure

```
aqi-predictor/
│
├── fetch_data.py       # Fetches real-time AQI data from WAQI API
├── train_model.py      # Trains Random Forest ML model
├── predict.py          # Makes 7-day predictions + health alerts
│
├── data/               # Stores fetched AQI data (CSV)
├── models/             # Stores trained ML model (.pkl)
├── outputs/            # Stores graphs and prediction reports
│
├── .env                # API key (not pushed to GitHub)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

**1. Clone the repository**

```bash
git clone https://github.com/Lakshyyyaaaaa/aqi-predictor.git
cd aqi-predictor
```

**2. Create and activate virtual environment**

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows
```

**3. Install dependencies**

```bash
pip install pandas numpy matplotlib seaborn scikit-learn requests openpyxl python-dotenv
```

**4. Get your free API key**

Go to https://aqicn.org/data-platform/token/ and get a free token.

Create a `.env` file in the root folder:

```
AQI_API_KEY=your_token_here
```

---

## ▶️ How to Run

**Step 1 — Fetch real-time data:**

```bash
python fetch_data.py
```

**Step 2 — Train the ML model:**

```bash
python train_model.py
```

**Step 3 — Generate predictions and alerts:**

```bash
python predict.py
```

---

## 📊 Model Performance

| Metric              | Score                   |
| ------------------- | ----------------------- |
| Algorithm           | Random Forest Regressor |
| Training samples    | 292                     |
| Testing samples     | 73                      |
| Mean Absolute Error | 8.94                    |
| R² Score            | 0.82                    |

> R² score of 0.82 means the model explains **82% of AQI variation** — considered a strong result for environmental prediction.

---

## 🚨 AQI Alert Levels

| AQI Range | Level                             |
| --------- | --------------------------------- |
| 0 - 50    | Good ✅                           |
| 51 - 100  | Moderate ⚠️                       |
| 101 - 150 | Unhealthy for Sensitive Groups 🟠 |
| 151 - 200 | Unhealthy 🔴                      |
| 201 - 300 | Very Unhealthy ☠️                 |
| 300+      | Hazardous ☢️                      |

---

## 📸 Sample Output

```
DELHI        → Avg 7-day AQI: 215.9 | Very Unhealthy ☠️
MUMBAI       → Avg 7-day AQI: 137.3 | Unhealthy for Sensitive Groups 🟠
BANGALORE    → Avg 7-day AQI: 183.5 | Unhealthy 🔴
JAIPUR       → Avg 7-day AQI: 175.0 | Unhealthy 🔴
```

---

## 🔮 Future Improvements

- [ ] Add more Indian cities
- [ ] Build a web dashboard using Flask/Streamlit
- [ ] Use LSTM (deep learning) for better time-series prediction
- [ ] Send automated email alerts when AQI crosses threshold
- [ ] Deploy on cloud (AWS/Heroku)

---

## 👨‍💻 Author

**Lakshya** — 3rd Year Computer Science Student  
GitHub: [@Lakshyyyaaaaa](https://github.com/Lakshyyyaaaaa)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
