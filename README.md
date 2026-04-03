# 🚖 NYC Ride Price Optimizer (Taxi vs Uber vs Lyft)

An end-to-end data analytics and machine learning project that predicts ride demand, estimates fares, and recommends the most cost-effective ride option across Local Taxi, Uber, and Lyft.

🔗 **Live App:** https://nyc-taxi-price-optimizer.streamlit.app/

---

## 📊 Project Overview

This project combines historical NYC taxi trip data sourced from AWS Open Data, KPI-driven analytics, and machine learning to build a demand-aware ride pricing system.

Users can select:
- Pickup zone
- Dropoff zone
- Day and hour (or use real-time)

The system:
- Retrieves route-level historical insights
- Predicts ride demand using a trained ML model
- Estimates fares for Taxi, Uber, and Lyft
- Recommends the cheapest option
- Displays KPI insights for better decision-making

---

## 💼 Business Problem

Ride prices fluctuate based on demand, time, and location. Riders often lack visibility into the most cost-effective option, while platforms need insights into pricing behavior and demand patterns.

This project solves that by integrating:
- Demand prediction
- Route-level pricing analytics
- KPI insights
- Real-time recommendation logic
- Interactive user interface

---

## 🚀 Key Features

### 🖥️ Streamlit Web App
- Route-based fare estimation
- Taxi vs Uber vs Lyft comparison
- Demand-aware recommendations
- Real-time or manual time selection
- KPI insights per route
- Clean, interactive UI

### 🧠 Machine Learning
- Model: **Random Forest Regressor**
- Target: Ride demand
- Performance: **R² ≈ 0.74**
- Features:
  - Zone
  - Weekday
  - Hour
  - Avg trip miles
  - Avg fare
  - Avg driver pay

### 📊 Power BI Dashboard
- Ride demand by hour
- Top pickup zones
- Average fare trends
- Weekday vs hour heatmap
- KPI dashboards

---

## 📦 Dataset

**Source:**
- NYC Taxi & Limousine Commission (TLC) FHVHV Trip Data
- Accessed via [Amazon Web Services](https://registry.opendata.aws/) Open Data Registry

**Link:**
- [https://registry.opendata.aws/nyc-taxi-data/](https://registry.opendata.aws/nyc-tlc-trip-records-pds/)

**Details:**
The dataset is provided in Parquet format and contains large-scale trip-level records including pickup/dropoff locations, timestamps, fares, driver pay, and trip distances.

**Processing Steps:**
- Removed invalid and outlier trips
- Mapped location IDs to taxi zones
- Engineered route-level and zone-level features
- Created summary tables for fast querying

---

## 📈 KPI Engineering

Key metrics used in analysis:

- `fare_per_mile`
- `fare_per_minute`
- `driver_pay_per_mile`
- `driver_share_pct`
- `take_rate_pct`
- `tip_pct`
- `speed_mph`
- `pickup_hour`
- `weekday`

---

## 📊 Summary Tables

### Route Summary
- Avg distance, time, fare
- Min/max fare
- Fare variability
- Driver pay

### Demand Summary
- Trips per hour
- Avg fare per hour
- Demand level (Low / Medium / High)

### Zone Summary
- Total trips
- Avg fare
- Fare per mile
- Driver pay
- Take rate & driver share
- Tip percentage
- Avg speed

---

## 🛠️ Tech Stack

- **Python**
- **Pandas, NumPy**
- **Scikit-learn**
- **Joblib**
- **Streamlit**
- **Power BI**
- **Git & GitHub**

---

## 📁 Project Structure
## ⚙️ How It Works

1. User selects pickup and dropoff zones
2. Historical route data is retrieved
3. ML model predicts ride demand
4. Fare estimates are computed for Taxi, Uber, and Lyft
5. System recommends the most cost-effective option based on demand and pricing

---

## 💡 Key Insights

- High demand significantly increases Uber and Lyft prices (surge pricing)
- Local Taxi fares remain relatively stable during peak demand
- Driver share and platform take rates vary across ride types

---

## 🔮 Future Improvements

- 🗺️ NYC zone map visualization
- ⚡ Upgrade to XGBoost
- 🌦️ Weather-based demand prediction
- 📈 “Best time to travel” feature
- 🔌 Real-time Uber/Lyft API integration

---

## 👤 Author

**Rutwij Thorat**  
MS in Data Science & Business Analytics  
Wayne State University  

- GitHub: https://github.com/kira2000  
- LinkedIn: www.linkedin.com/in/rutwij-thorat1
If you found this project useful, consider giving it a ⭐ on GitHub!
