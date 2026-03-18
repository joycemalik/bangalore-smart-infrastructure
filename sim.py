import requests
import time
import random

TELEMETRY_URL = "http://localhost:8000/telemetry"

locations = [
    {
        "name": "Silk Board Junction",
        "lat": 12.9176,
        "lng": 77.6233,
        "type": "traffic",
        "generate": lambda: random.uniform(80.0, 100.0)
    },
    {
        "name": "Hebbal Flyover",
        "lat": 13.0358,
        "lng": 77.5970,
        "type": "bridge",
        "generate": lambda: 0.7 if random.random() < 0.1 else random.uniform(0.95, 1.0)
    },
    {
        "name": "Electronic City Flyover",
        "lat": 12.8488,
        "lng": 77.6599,
        "type": "speed",
        "generate": lambda: random.uniform(20.0, 80.0)
    },
    {
        "name": "Marathahalli ORR",
        "lat": 12.9562,
        "lng": 77.7011,
        "type": "traffic",
        "generate": lambda: random.uniform(60.0, 95.0)
    }
]

def simulate():
    print("Starting simulation...")
    while True:
        for loc in locations:
            value = loc["generate"]()
            data = {
                "location": loc["name"],
                "type": loc["type"],
                "value": value,
                "lat": loc["lat"],
                "lng": loc["lng"]
            }
            try:
                response = requests.post(TELEMETRY_URL, json=data)
                print(f"Sent {loc['name']} ({loc['type']}): {value:.2f} - Status: {response.status_code}")
            except Exception as e:
                print(f"Failed to send data to {TELEMETRY_URL}: {e}")
        time.sleep(2)

if __name__ == "__main__":
    simulate()
