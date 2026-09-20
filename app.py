import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="AQI Forecast", layout="centered")

# Load model
model = joblib.load('random_forest_aqi_model.pkl')

st.title("Air Quality PM2.5 Forecast Dashboard")
st.caption(
    "Machine learning forecasting using Indian multi-city sensor records."
)

# Sidebar inputs
st.sidebar.header("Input Sensor Readings")
pm10 = st.sidebar.number_input("PM10 (µg/m³)", min_value=0.0, value=120.0)
pm25_lag1 = st.sidebar.number_input(
    "Yesterday's PM2.5 (µg/m³)", min_value=0.0, value=95.0
)
no2 = st.sidebar.number_input(
    "Nitrogen Dioxide - NO2 (µg/m³)", min_value=0.0, value=35.0
)
so2 = st.sidebar.number_input(
    "Sulfur Dioxide - SO2 (µg/m³)", min_value=0.0, value=12.0
)
co = st.sidebar.number_input(
    "Carbon Monoxide - CO (µg/m³)", min_value=0.0, value=1.5
)
o3 = st.sidebar.number_input("Ozone - O3 (µg/m³)", min_value=0.0, value=40.0)
month = st.sidebar.slider("Month", 1, 12, 11)
is_weekend = st.sidebar.selectbox("Day Type", [0, 1], format_func=lambda x: "Weekend" if x == 1 else "Weekday")

# Inference
if st.button("Generate Forecast", type="primary"):
    input_df = pd.DataFrame(
        [[pm10, o3, no2, so2, co, month, is_weekend, pm25_lag1]],
        columns=[
            'pm10',
            'o3',
            'no2',
            'so2',
            'co',
            'month',
            'is_weekend',
            'pm25_lag1',
        ],
    )

    pred = model.predict(input_df)[0]

    st.subheader("Forecast Results")
    st.metric(label="Predicted PM2.5 (Next 24h)", value=f"{pred:.1f} µg/m³")

    # Indian National Air Quality Index (NAQI) PM2.5 Category Mapping
    if pred <= 30:
        st.success("Category: *Good* (0-30 µg/m³) — Minimal health impact.")
    elif pred <= 60:
        st.info(
            "Category: *Satisfactory* (31-60 µg/m³) — Minor breathing"
            " discomfort to sensitive people."
        )
    elif pred <= 90:
        st.warning(
            "Category: *Moderate* (61-90 µg/m³) — Breathing discomfort with"
            " lung or heart disease."
        )
    elif pred <= 120:
        st.warning(
            "Category: *Poor* (91-120 µg/m³) — Breathing discomfort to most"
            " people on prolonged exposure."
        )
    elif pred <= 250:
        st.error(
            "Category: *Very Poor* (121-250 µg/m³) — Respiratory illness on"
            " prolonged exposure."
        )
    else:
        st.error(
            "Category: *Severe* (>250 µg/m³) — Serious health impacts even for"
            " healthy individuals."
        )