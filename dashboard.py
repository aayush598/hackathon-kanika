import streamlit as st
import requests
import pandas as pd
import time

# Flask server API
SERVER_URL = "http://127.0.0.1:3000/api/get-latest-sensor-data"

st.title("Live Sensor Data Dashboard")

# **Create placeholders for latest values**
latest_hr = st.empty()
latest_spo2 = st.empty()
latest_temp = st.empty()

# **Subheaders for graphs**
st.subheader("Heart Rate")
hr_chart = st.line_chart(pd.DataFrame({"timestamp": [], "heartRate": []}).set_index("timestamp"))

st.subheader("SpO2 Level")
spo2_chart = st.line_chart(pd.DataFrame({"timestamp": [], "spO2": []}).set_index("timestamp"))

st.subheader("Temperature")
temp_chart = st.line_chart(pd.DataFrame({"timestamp": [], "temperature": []}).set_index("timestamp"))

while True:
    try:
        # Fetch data from the Flask API
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            data = response.json()

            if data:
                df = pd.DataFrame(data)
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

                # **Get the latest sensor readings**
                latest_values = df.iloc[-1]  # Last row (most recent data)

                # **Update text placeholders with current values**
                latest_hr.subheader(f"Current Heart Rate: {latest_values['heartRate']} BPM")
                latest_spo2.subheader(f"Current SpO2 Level: {latest_values['spO2']}%")
                latest_temp.subheader(f"Current Temperature: {latest_values['temperature']}°C")

                # **Update graphs with only the latest 10 values**
                hr_chart.line_chart(df.set_index("timestamp")["heartRate"])
                spo2_chart.line_chart(df.set_index("timestamp")["spO2"])
                temp_chart.line_chart(df.set_index("timestamp")["temperature"])

    except Exception as e:
        st.error(f"Error fetching data: {e}")

    time.sleep(2)  # Refresh every 2 seconds
