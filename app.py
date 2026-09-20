import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title='Air Quality (PM2.5) Forecaster',
    page_icon='🌫️',
    layout='wide',
)

# --------------------------------------------------
# 2. Model Mapping & Dynamic Loader
# --------------------------------------------------
MODEL_MAP = {
    'Overall India': 'random_forest_aqi_model.pkl',
    'Delhi': 'rf_model_delhi.pkl',
    'Hyderabad': 'rf_model_hyderabad.pkl',
    'Mumbai': 'rf_model_mumbai.pkl',
    'Chennai': 'rf_model_chennai.pkl',
    'Lucknow': 'rf_model_lucknow.pkl',
    'Patna': 'rf_model_patna.pkl',
}


@st.cache_resource
def get_model(filename):
  if not os.path.exists(filename):
    return None
  return joblib.load(filename)


# --------------------------------------------------
# 3. Sidebar Controls
# --------------------------------------------------
st.sidebar.title('⚙️ Configuration')

# City / Region Filter
selected_region = st.sidebar.selectbox(
    'Select Forecast Region / City',
    options=list(MODEL_MAP.keys()),
    index=0,
    help='Choose Overall India for a national baseline, or a specific city model.',
)

model_filename = MODEL_MAP[selected_region]
model = get_model(model_filename)

if model is not None:
  st.sidebar.success(f'Loaded model: {model_filename}')
else:
  st.sidebar.error(f'File {model_filename} not found in root directory.')

st.sidebar.markdown('---')
st.sidebar.subheader('Temporal Parameters')
selected_month = st.sidebar.slider('Month of the Year', 1, 12, 10)
is_weekend = st.sidebar.radio('Is it a weekend?', ('No', 'Yes'))
is_weekend_val = 1 if is_weekend == 'Yes' else 0

# --------------------------------------------------
# 4. Main Dashboard Header
# --------------------------------------------------
st.title('🌫️ Air Quality PM2.5 Prediction Dashboard')
st.markdown(
    f'Forecasting particulate matter concentration tailored for: *{selected_region}*'
)
st.markdown('---')

# --------------------------------------------------
# 5. Pollutant Inputs
# --------------------------------------------------
st.subheader('Enter Current Atmospheric & Pollutant Levels')

col1, col2 = st.columns(2)

with col1:
  pm10 = st.slider(
      'PM10 (µg/m³)', min_value=0.0, max_value=500.0, value=110.0, step=1.0
  )
  no2 = st.slider(
      'Nitrogen Dioxide - NO2 (µg/m³)',
      min_value=0.0,
      max_value=300.0,
      value=35.0,
      step=0.5,
  )
  so2 = st.slider(
      'Sulfur Dioxide - SO2 (µg/m³)',
      min_value=0.0,
      max_value=200.0,
      value=15.0,
      step=0.5,
  )

with col2:
  co = st.slider(
      'Carbon Monoxide - CO (mg/m³)',
      min_value=0.0,
      max_value=20.0,
      value=1.2,
      step=0.1,
  )
  o3 = st.slider(
      'Ozone - O3 (µg/m³)', min_value=0.0, max_value=250.0, value=28.0, step=0.5
  )
  pm25_lag1 = st.slider(
      'Previous Day PM2.5 - Lag 1 (µg/m³)',
      min_value=0.0,
      max_value=500.0,
      value=65.0,
      step=1.0,
  )

# --------------------------------------------------
# 6. AQI Severity Helper
# --------------------------------------------------
def get_aqi_category(pm25_value):
  if pm25_value <= 30:
    return 'Good (0-30)', '#2ecc71'
  elif pm25_value <= 60:
    return 'Satisfactory (31-60)', '#a8e6cf'
  elif pm25_value <= 90:
    return 'Moderate (61-90)', '#f1c40f'
  elif pm25_value <= 120:
    return 'Poor (91-120)', '#e67e22'
  elif pm25_value <= 250:
    return 'Very Poor (121-250)', '#e74c3c'
  else:
    return 'Severe (250+)', '#78281f'


# --------------------------------------------------
# 7. Prediction Trigger
# --------------------------------------------------
st.markdown('---')

if st.button('Generate Forecast', use_container_width=True):
  if model is None:
    st.error(
        f"Unable to run prediction because '{model_filename}' is missing. Please ensure the file is committed to your repository."
    )
  else:
    input_df = pd.DataFrame(
        [[
            pm10,
            o3,
            no2,
            so2,
            co,
            selected_month,
            is_weekend_val,
            pm25_lag1,
        ]],
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

    prediction = float(model.predict(input_df)[0])
    category_label, color_code = get_aqi_category(prediction)

    st.subheader('Forecast Result')
    res_col1, res_col2 = st.columns(2)

    with res_col1:
      st.metric(
          label=f'Predicted PM2.5 for {selected_region}',
          value=f'{prediction:.2f} µg/m³',
          delta=f'{prediction - pm25_lag1:+.2f} vs yesterday',
      )

    with res_col2:
      st.markdown(
          f"""
            <div style="background-color: {color_code}; padding: 18px; border-radius: 8px; text-align: center;">
                <h4 style="color: black; margin: 0;">Category: {category_label}</h4>
            </div>
            """,
          unsafe_allow_html=True,
      )