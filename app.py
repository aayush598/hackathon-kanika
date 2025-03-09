from flask import Flask, request, jsonify
import sqlite3
import time

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            heartRate INTEGER,
            spO2 INTEGER,
            temperature REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Run database setup on start

# API to receive sensor data from ESP32
@app.route("/api/sensor-data", methods=["POST"])
def receive_sensor_data():
    data = request.json
    timestamp = int(time.time())  # Get current timestamp

    # Store data in SQLite
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data (timestamp, heartRate, spO2, temperature) VALUES (?, ?, ?, ?)",
                   (timestamp, data["heartRate"], data["spO2"], data["temperature"]))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data stored successfully"}), 201

# API to fetch the latest 10 sensor readings
@app.route("/api/get-latest-sensor-data", methods=["GET"])
def get_latest_sensor_data():
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, heartRate, spO2, temperature FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to JSON (reverse order for correct time sequence)
    data = [{"timestamp": row[0], "heartRate": row[1], "spO2": row[2], "temperature": row[3]} for row in reversed(rows)]
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
