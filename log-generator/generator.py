import random
import time
import requests
from datetime import datetime

endpoints = ["/login", "/dashboard", "/api/data", "/logout"]

API_URL = "http://backend-service:8000/predict"

def generate_log():
    endpoint = random.choice(endpoints)

    response_time = random.randint(100, 300)
    status = 200

    if random.random() < 0.1:
        response_time = random.randint(800, 2000)
        status = random.choice([500, 502, 503])

    return {
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "response_time": response_time,
        "status": status
    }

def send_log():
    while True:
        log = generate_log()

        payload = {
            "response_time": log["response_time"],
            "status": log["status"]
        }

        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()

            if result["anomaly"]:
                print(f"🚨 Anomaly Detected: {log}")
            else:
                print(f"✅ Normal: {log}")

        except Exception as e:
            print("Error:", e)

        time.sleep(1)

if __name__ == "__main__":
    send_log()