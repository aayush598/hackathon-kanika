import streamlit as st
import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Flask server API
SERVER_URL = "http://127.0.0.1:3000/api/get-latest-sensor-data"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

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

# Placeholder for AI Analysis
st.subheader("Gemini AI Analysis")
ai_analysis = st.empty()

def fetch_latest_data():
    """Fetch latest 10 sensor readings from Flask API."""
    response = requests.get(SERVER_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def analyze_with_gemini(data):
    """Send the latest 10 sensor data points to Gemini AI for analysis."""
    if not data:
        return "No data available for analysis."

    prompt = "Analyze the following sensor readings and provide insights:\n\n"
    for entry in data:
        prompt += f"- Time: {entry['timestamp']}, Heart Rate: {entry['heartRate']} BPM, SpO2: {entry['spO2']}%, Temperature: {entry['temperature']}°C\n"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(GEMINI_URL, json=payload, headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        analysis = response.json()
        return analysis.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response from AI.")
    else:
        return f"Error: {response.text}"

# **Initialize session state variables**
if 'latest_data' not in st.session_state:
    st.session_state.latest_data = []

if 'gemini_result' not in st.session_state:  # Changed key to "gemini_result"
    st.session_state.gemini_result = None  # Prevents repeated API calls

data = fetch_latest_data()
if data:
    st.session_state.latest_data = data

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    # **Update text placeholders with current values**
    latest_values = df.iloc[-1]
    latest_hr.subheader(f"Current Heart Rate: {latest_values['heartRate']} BPM")
    latest_spo2.subheader(f"Current SpO2 Level: {latest_values['spO2']}%")
    latest_temp.subheader(f"Current Temperature: {latest_values['temperature']}°C")

    # **Update graphs with latest 10 values**
    hr_chart.line_chart(df.set_index("timestamp")["heartRate"])
    spo2_chart.line_chart(df.set_index("timestamp")["spO2"])
    temp_chart.line_chart(df.set_index("timestamp")["temperature"])

# **Button for AI Analysis (Fixed)**
if st.button("Analyze Data with Gemini AI", key="analyze_button"):  # Unique key for button
    st.session_state.gemini_result = analyze_with_gemini(st.session_state.latest_data)  # Store analysis

# Display Gemini Analysis (if available)
if st.session_state.gemini_result:
    ai_analysis.write(st.session_state.gemini_result)

# **Auto-refresh every 2 seconds, but NOT triggering Gemini API again**
time.sleep(2)
st.rerun()
