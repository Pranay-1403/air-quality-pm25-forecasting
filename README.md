# Air Quality PM2.5 Forecast Dashboard

## Problem Statement
Air pollution is a critical public health concern. This project forecasts next-day PM2.5 particulate levels across urban monitoring stations to help individuals and local authorities evaluate air quality risks.

## Dataset
- *Source:* India Multi-City Air Quality Dataset (Consolidated sensor logs, 96,000+ records)
- *Features Tracked:* PM10, O3, NO2, SO2, CO, PM2.5 lag metrics, and calendar features.

## Model Performance

| Model | R² Score | MAE (µg/m³) | RMSE (µg/m³) |
| :--- | :---: | :---: | :---: |
| Multiple Linear Regression | 0.7274 | 24.89 | 43.36 |
| Random Forest Regressor | 0.7131 | 23.05 | 44.48 |

- *Key Takeaway:* The Random Forest Regressor reduced typical absolute prediction error to 23.05 µg/m³. Recent historical pollution levels (pm25_lag1) proved to be the primary driving factor.

## Web Application
An interactive dashboard built with *Streamlit* allows users to input sensor metrics and receive:
1. Next 24-hour PM2.5 prediction.
2. National Air Quality Index (NAQI) health advisory warnings.

## How to Run Locally
1. Clone this repository:
   ```bash
   git clone <your-github-repo-url>
   cd <repo-folder>

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Run the Streamlit app:
    ```bash
    streamlit run app.py

"""