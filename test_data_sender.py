import requests
import random
import time

SERVER_URL = "http://127.0.0.1:3000/api/sensor-data"

while True:
    data = {
        "heartRate": random.randint(60, 100),
        "spO2": random.randint(95, 100),
        "temperature": round(random.uniform(35.5, 39.0), 2)
    }
    
    response = requests.post(SERVER_URL, json=data)
    
    if response.status_code == 200:
        print(f"Sent: {data}")
    else:
        print(f"Failed to send data: {response.status_code}")

    time.sleep(5)  # Send data every 5 seconds
