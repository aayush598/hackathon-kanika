import streamlit as st
import requests
import pandas as pd
import time

# Flask server URL
SERVER_URL = "http://127.0.0.1:3000/api/get-sensor-data"

st.title("Live Sensor Data Dashboard")

# Initialize DataFrame with default values to prevent Altair warnings
df = pd.DataFrame({"timestamp": [0], "heartRate": [0], "spO2": [0], "temperature": [0]})
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

# Create placeholders for each graph
st.subheader("Heart Rate")
hr_chart = st.line_chart(df.set_index("timestamp")["heartRate"])

st.subheader("SpO2 Level")
spo2_chart = st.line_chart(df.set_index("timestamp")["spO2"])

st.subheader("Temperature")
temp_chart = st.line_chart(df.set_index("timestamp")["temperature"])

while True:
    try:
        # Fetch the latest sensor data
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            data = response.json()

            if data:
                df = pd.DataFrame(data)
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

                # Update charts only if new data exists
                hr_chart.line_chart(df.set_index("timestamp")["heartRate"])
                spo2_chart.line_chart(df.set_index("timestamp")["spO2"])
                temp_chart.line_chart(df.set_index("timestamp")["temperature"])

    except Exception as e:
        st.error(f"Error fetching data: {e}")

    time.sleep(2)  # Refresh every 2 seconds
