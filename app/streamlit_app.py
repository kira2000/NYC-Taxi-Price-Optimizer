import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

st.set_page_config(page_title="NYC Ride Price Comparison App", layout="wide")

st.title("NYC Ride Price Optimizer (Taxi vs Uber vs Lyft)")
st.write(
    "Compare estimated Local Taxi, Uber, and Lyft fares using route history, "
    "predicted demand, and KPI-based insights."
)

# -----------------------------
# Load data
# -----------------------------
route_summary = pd.read_csv("../data/route_summary.csv")
demand_summary = pd.read_csv("../data/demand_summary.csv")
zone_summary = pd.read_csv("../data/zone_summary.csv")
demand_dataset = pd.read_csv("../data/demand_dataset.csv")

model = joblib.load("../models/nyc_taxi_demand_model.pkl")

# -----------------------------
# Recreate encoders from training data
# -----------------------------
le_zone = LabelEncoder()
le_weekday = LabelEncoder()

le_zone.fit(demand_dataset["Zone"])
le_weekday.fit(demand_dataset["weekday"])

# -----------------------------
# Current live time
# -----------------------------
now = datetime.now()
current_hour = now.hour
current_weekday = now.strftime("%A")

pickup_options = sorted(route_summary["pickup_zone"].dropna().unique())
dropoff_options = sorted(route_summary["dropoff_zone"].dropna().unique())
weekday_options = ["Monday", "Tuesday", "Wednesday",
                   "Thursday", "Friday", "Saturday", "Sunday"]

# -----------------------------
# Inputs inside form
# -----------------------------
st.subheader("Trip Inputs")

pickup_options = sorted(route_summary["pickup_zone"].dropna().unique())
dropoff_options = sorted(route_summary["dropoff_zone"].dropna().unique())
weekday_options = ["Monday", "Tuesday", "Wednesday",
                   "Thursday", "Friday", "Saturday", "Sunday"]

col1, col2 = st.columns(2)

with col1:
    pickup_zone = st.selectbox("Select Pickup Zone", pickup_options)

with col2:
    dropoff_zone = st.selectbox("Select Dropoff Zone", dropoff_options)

use_live_time = st.checkbox("Use current day and hour", value=True)

if use_live_time:
    weekday = current_weekday
    hour = current_hour
    st.info(f"Using current time: {weekday}, {hour}:00")
else:
    col3, col4 = st.columns(2)
    with col3:
        weekday = st.selectbox("Select Day", weekday_options)
    with col4:
        hour = st.slider("Select Hour", 0, 23, 12)

search_clicked = st.button("Search")

if st.button("Reset"):
    st.experimental_rerun()

# -----------------------------
# Only run logic after Search
# -----------------------------
if search_clicked:
    route_match = route_summary[
        (route_summary["pickup_zone"] == pickup_zone) &
        (route_summary["dropoff_zone"] == dropoff_zone)
    ]

    if route_match.empty:
        st.warning(
            "No historical route match found for this pickup/dropoff combination.")
        st.stop()

    route_row = route_match.iloc[0]

    avg_miles = float(route_row["avg_miles"])
    avg_time_minutes = float(route_row["avg_time_minutes"])
    avg_fare = float(route_row["avg_fare"])
    min_fare = float(route_row["min_fare"])
    max_fare = float(route_row["max_fare"])
    avg_driver_pay = float(route_row["avg_driver_pay"])
    avg_fare_per_mile = float(route_row["avg_fare_per_mile"])
    avg_speed_mph = float(route_row["avg_speed_mph"])

    demand_match = demand_summary[demand_summary["pickup_hour"] == hour]
    demand_level = demand_match.iloc[0]["demand_level"] if not demand_match.empty else "Medium"

    zone_match = zone_summary[zone_summary["zone"] == pickup_zone]
    if not zone_match.empty:
        zone_row = zone_match.iloc[0]
        avg_take_rate_pct = float(zone_row["avg_take_rate_pct"])
        avg_driver_share_pct = float(zone_row["avg_driver_share_pct"])
        avg_tip_pct = float(zone_row["avg_tip_pct"])
    else:
        avg_take_rate_pct = 25.0
        avg_driver_share_pct = 75.0
        avg_tip_pct = 5.0

    if pickup_zone not in le_zone.classes_:
        st.warning(
            "Selected pickup zone is not available in the ML training dataset.")
        st.stop()

    zone_encoded = le_zone.transform([pickup_zone])[0]
    weekday_encoded = le_weekday.transform([weekday])[0]

    model_input = pd.DataFrame([{
        "Zone": zone_encoded,
        "weekday": weekday_encoded,
        "hour": hour,
        "avg_trip_miles": avg_miles,
        "avg_fare": avg_fare,
        "avg_driver_pay": avg_driver_pay
    }])

    predicted_rides = float(model.predict(model_input)[0])

    # -----------------------------
    # Pricing logic
    # -----------------------------
    local_taxi_base = 3.50 + (2.80 * avg_miles)

    if demand_level == "Low":
        taxi_mult = 1.00
        uber_mult = 1.00
        lyft_mult = 0.98
    elif demand_level == "Medium":
        taxi_mult = 1.05
        uber_mult = 1.20
        lyft_mult = 1.15
    else:
        taxi_mult = 1.10
        uber_mult = 1.45
        lyft_mult = 1.35

    local_taxi_fare = local_taxi_base * taxi_mult
    uber_fare = (5.00 + 3.20 * avg_miles) * uber_mult
    lyft_fare = (4.50 + 3.00 * avg_miles) * lyft_mult

    fare_options = {
        "Local Taxi": local_taxi_fare,
        "Uber": uber_fare,
        "Lyft": lyft_fare
    }
    cheapest_option = min(fare_options, key=fare_options.get)

    # -----------------------------
    # Outputs
    # -----------------------------
    st.subheader("Route Summary")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Avg Trip Distance", f"{avg_miles:.2f} miles")
    r2.metric("Avg Trip Time", f"{avg_time_minutes:.1f} min")
    r3.metric("Historical Avg Fare", f"${avg_fare:.2f}")
    r4.metric("Fare Range", f"${min_fare:.2f} - ${max_fare:.2f}")

    st.subheader("Demand Prediction")

    d1, d2 = st.columns(2)
    d1.metric("Predicted Ride Demand", f"{int(round(predicted_rides))} rides")
    d2.metric("Demand Level", demand_level)

    st.subheader("Ride Price Comparison")

    p1, p2, p3 = st.columns(3)

    def highlight(label, value, is_best):
        if is_best:
            st.success(f"{label}: ${value:.2f} ⭐")
        else:
            st.metric(label, f"${value:.2f}")

    with p1:
        highlight("Local Taxi", local_taxi_fare,
                  cheapest_option == "Local Taxi")

    with p2:
        highlight("Uber", uber_fare, cheapest_option == "Uber")

    with p3:
        highlight("Lyft", lyft_fare, cheapest_option == "Lyft")

    # -----------------------------
    # Price Table
    # -----------------------------
    st.subheader("Price Comparison Table")

    comparison_df = pd.DataFrame({
        "Service": ["Local Taxi", "Uber", "Lyft"],
        "Estimated Fare ($)": [local_taxi_fare, uber_fare, lyft_fare]
    })

    st.dataframe(comparison_df)

    # -----------------------------
    # KPI Section
    # -----------------------------
    st.subheader("Driver + Platform KPI Insights")

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Avg Driver Pay", f"${avg_driver_pay:.2f}")
    k2.metric("Fare per Mile", f"${avg_fare_per_mile:.2f}")
    k3.metric("Driver Share %", f"{avg_driver_share_pct:.1f}%")
    k4.metric("Take Rate %", f"{avg_take_rate_pct:.1f}%")
    k5.metric("Tip %", f"{avg_tip_pct:.1f}%")
    k6.metric("Avg Speed", f"{avg_speed_mph:.1f} mph")

    # -----------------------------
    # Best Option
    # -----------------------------
    st.subheader("Best Option")
    st.success(f"👉 Recommended: {cheapest_option}")

    # -----------------------------
    # Recommendation
    # -----------------------------
    st.subheader("Recommendation")

    if cheapest_option == "Local Taxi" and demand_level == "High":
        st.success("Take a Local Taxi — surge pricing likely on Uber/Lyft.")
    elif cheapest_option == "Uber":
        st.success("Uber is the cheapest option.")
    elif cheapest_option == "Lyft":
        st.success("Lyft is the cheapest option.")
    else:
        st.success("Local Taxi is the most cost-effective.")

    st.caption(
        "Note: Uber and Lyft prices are estimated using historical data and demand predictions."
    )
