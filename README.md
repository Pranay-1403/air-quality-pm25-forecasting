# 🌫️ Multi-City Air Quality (PM2.5) Forecasting Dashboard

An interactive end-to-end Machine Learning web application built with *Streamlit* and *Scikit-Learn* to forecast Particulate Matter 2.5 ($PM_{2.5}$) levels across major Indian metropolitan hubs and nationwide.

---

## 📌 Project Overview

Air pollution levels vary significantly across geographical regions due to local industrial output, vehicular emissions, and seasonal weather patterns. This project provides:
- *National Baseline Model*: A generalized model capturing overall India trends.
- *City-Specific Specialized Models: Dedicated Random Forest regressors tuned to unique localized conditions for **Delhi, Hyderabad, Mumbai, Chennai, Lucknow, and Patna*.
- *Interactive Web Interface*: Real-time predictions based on key atmospheric pollutants, calendar months, and lag features with standard CPCB AQI severity categorization.

---

## 🛠️ Tech Stack & Libraries

- *Language*: Python
- *Libraries*: Pandas, NumPy, Scikit-Learn, Joblib, Streamlit
- *Model*: RandomForestRegressor
- *Deployment*: Streamlit Community Cloud

---

## 📂 Project Structure

```text
├── app.py                            # Main Streamlit application
├── Multi_City_Air_Quality.ipynb      # Notebook for model training & data processing
├── random_forest_aqi_model.pkl       # Baseline model for Overall India
├── rf_model_delhi.pkl                # City-specific model for Delhi
├── rf_model_hyderabad.pkl            # City-specific model for Hyderabad
├── rf_model_mumbai.pkl               # City-specific model for Mumbai
├── rf_model_chennai.pkl              # City-specific model for Chennai
├── rf_model_lucknow.pkl              # City-specific model for Lucknow
├── rf_model_patna.pkl                # City-specific model for Patna
├── requirements.txt                  # Python package dependencies
└── README.md                         # Project documentation

## How to Run Locally
1. Clone this repository:
   ```bash
   git clone <https://github.com/Pranay-1403/air-quality-pm25-forecasting.git>
   cd <repo-folder>

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Run the Streamlit app:
    ```bash
    streamlit run app.py

"""