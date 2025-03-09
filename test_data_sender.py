import requests
import random
import time

SERVER_URL = "http://127.0.0.1:3000/api/sensor-data"

while True:
    data = {
        "heartRate": random.randint(60, 100),
        "spO2": random.randint(95, 100),
        "temperature": round(random.uniform(36.0, 38.5), 2)
    }

    response = requests.post(SERVER_URL, json=data)
    
    if response.status_code == 201:
        print("Sent:", data)
    else:
        print("Failed to send data:", response.text)

    time.sleep(5)  # Send data every 5 seconds
