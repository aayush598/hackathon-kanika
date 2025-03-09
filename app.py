from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for Streamlit frontend

# Store sensor data in-memory (for demonstration)
sensor_data = []

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    global sensor_data
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Append timestamped data
    data["timestamp"] = time.time()
    sensor_data.append(data)

    # Keep only the last 50 readings to prevent excessive memory usage
    sensor_data = sensor_data[-50:]

    return jsonify({"message": "Data received successfully"}), 200

@app.route('/api/get-sensor-data', methods=['GET'])
def get_sensor_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
