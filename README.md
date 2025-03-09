# **ESP32 Sensor Data Streaming with Flask & Streamlit** 🚀

This project collects **heart rate, SpO2, and temperature** sensor data from an **ESP32**, sends it to a **Flask server**, and visualizes the data in **real-time** using **Streamlit**.

## 📌 **Project Features**

✅ ESP32 collects sensor data and sends it via HTTP POST.  
✅ Flask backend stores and serves the data via REST API.  
✅ Streamlit frontend displays **live graphs** of heart rate, SpO2, and temperature.  
✅ A test script sends **dummy sensor data** for testing.

---

## 🛠 **Installation & Setup**

### 1️⃣ Install Required Packages

Make sure you have **Python 3.8+** installed. Then, install dependencies:

```sh
pip install flask flask-cors streamlit requests pandas
```

### 2️⃣ Run the Flask Backend

```sh
python app.py
```

This will start the **Flask API server** at `http://127.0.0.1:3000`.

### 3️⃣ Start the Streamlit Dashboard

```sh
streamlit run dashboard.py
```

This opens a real-time **sensor data visualization dashboard** in your browser.

### 4️⃣ (Optional) Run the Test Script

If you don’t have an ESP32 yet, use the test script to send **dummy sensor data**:

```sh
python test_data_sender.py
```

---

## 🔗 **Project Structure**

```
📂 ESP32-Sensor-Dashboard
│── app.py               # Flask backend
│── dashboard.py         # Streamlit frontend
│── test_data_sender.py  # Script to send test data
│── README.md            # Project documentation
```

---

## 🖥 **ESP32 Code (Arduino)**

1️⃣ Connect an **MLX90614 temperature sensor** to the ESP32 using I2C (SDA: GPIO4, SCL: GPIO5).  
2️⃣ Connect to **WiFi** and send sensor data to `http://192.168.X.X:3000/api/sensor-data`.  
3️⃣ Use **randomized heart rate & SpO2 values** for simulation.

---

## 📊 **Live Dashboard** (Built with Streamlit)

The dashboard updates every **2 seconds** and displays:  
📈 **Heart Rate Graph**  
📉 **SpO2 Level Graph**  
🌡 **Temperature Graph**

---

## ⚡ **API Endpoints**

### **1️⃣ Send Sensor Data (ESP32 → Flask)**

- **URL:** `POST /api/sensor-data`
- **Payload:**
  ```json
  {
    "heartRate": 75,
    "spO2": 98,
    "temperature": 36.5
  }
  ```
- **Response:**
  ```json
  { "message": "Data received successfully" }
  ```

### **2️⃣ Get Live Sensor Data (Streamlit → Flask)**

- **URL:** `GET /api/get-sensor-data`
- **Response:**
  ```json
  [
    {
      "heartRate": 72,
      "spO2": 97,
      "temperature": 36.7,
      "timestamp": 1710000000
    },
    {
      "heartRate": 78,
      "spO2": 99,
      "temperature": 36.8,
      "timestamp": 1710000020
    }
  ]
  ```

---

## 🚀 **Future Enhancements**

🔹 Add more sensor support (ECG, Blood Pressure).  
🔹 Store data in a database (SQLite, PostgreSQL).  
🔹 Add user authentication for secure access.

---

## 🎯 **Contributing**

Feel free to contribute by opening issues or submitting pull requests!

---

## 📜 **License**

This project is open-source and available under the **MIT License**.
