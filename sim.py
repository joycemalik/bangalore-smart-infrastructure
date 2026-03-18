import requests
import time
import random
import copy

API_URL = "http://localhost:8000/update"

# ──────────────────────────────────────────────────────────────
# ASSET DEFINITIONS
# ──────────────────────────────────────────────────────────────

HIGHWAYS = [
    {
        "id": "HWY-ORR-1",
        "name": "ORR Stretch (Silk Board → Marathahalli)",
        "path": [[12.9176, 77.6233], [12.9250, 77.6350], [12.9350, 77.6450], [12.9562, 77.7011]],
        "speed_kmh": 35.0,
        "congestion_pct": 70.0,
        "lanes": 6,
        "status": "congested",
        "vehicle_count": 4200,
    },
    {
        "id": "HWY-HOSUR-1",
        "name": "Hosur Road Elevated",
        "path": [[12.9176, 77.6233], [12.8800, 77.6400], [12.8488, 77.6599]],
        "speed_kmh": 45.0,
        "congestion_pct": 50.0,
        "lanes": 4,
        "status": "normal",
        "vehicle_count": 2800,
    },
    {
        "id": "HWY-AIRPORT-1",
        "name": "Airport Road (Hebbal → Yelahanka)",
        "path": [[13.0358, 77.5970], [13.0600, 77.5950], [13.1000, 77.5900]],
        "speed_kmh": 55.0,
        "congestion_pct": 30.0,
        "lanes": 6,
        "status": "normal",
        "vehicle_count": 3100,
    },
]

ROADS = [
    {
        "id": "RD-MG-1",
        "name": "MG Road",
        "path": [[12.9730, 77.5950], [12.9735, 77.6100]],
        "speed_kmh": 25.0,
        "congestion_pct": 65.0,
        "lanes": 4,
        "status": "congested",
        "vehicle_count": 1800,
    },
    {
        "id": "RD-INDNR-1",
        "name": "Indiranagar 100ft Road",
        "path": [[12.9780, 77.6380], [12.9650, 77.6380]],
        "speed_kmh": 30.0,
        "congestion_pct": 55.0,
        "lanes": 4,
        "status": "congested",
        "vehicle_count": 1500,
    },
    {
        "id": "RD-KRMG-1",
        "name": "Koramangala 80ft Road",
        "path": [[12.9340, 77.6230], [12.9400, 77.6300]],
        "speed_kmh": 22.0,
        "congestion_pct": 72.0,
        "lanes": 3,
        "status": "congested",
        "vehicle_count": 1200,
    },
    {
        "id": "RD-TUMKUR-1",
        "name": "Tumkur Road",
        "path": [[13.0250, 77.5350], [13.0450, 77.5100]],
        "speed_kmh": 40.0,
        "congestion_pct": 45.0,
        "lanes": 4,
        "status": "normal",
        "vehicle_count": 2100,
    },
]

BRIDGES = [
    {
        "id": "BR-HEBBAL-1",
        "name": "Hebbal Flyover",
        "lat": 13.0358,
        "lng": 77.5970,
        "health_index": 0.92,
        "vibration_hz": 4.5,
        "load_tons": 85.0,
        "last_inspection": "2026-02-15",
        "status": "healthy",
    },
    {
        "id": "BR-SILK-1",
        "name": "Silk Board Flyover",
        "lat": 12.9176,
        "lng": 77.6233,
        "health_index": 0.88,
        "vibration_hz": 5.2,
        "load_tons": 110.0,
        "last_inspection": "2026-01-28",
        "status": "healthy",
    },
    {
        "id": "BR-KRPURAM-1",
        "name": "KR Puram Bridge",
        "lat": 13.0010,
        "lng": 77.6740,
        "health_index": 0.95,
        "vibration_hz": 3.8,
        "load_tons": 75.0,
        "last_inspection": "2026-03-01",
        "status": "healthy",
    },
    {
        "id": "BR-NAYANH-1",
        "name": "Nayandahalli Junction Bridge",
        "lat": 12.9450,
        "lng": 77.5250,
        "health_index": 0.90,
        "vibration_hz": 4.0,
        "load_tons": 60.0,
        "last_inspection": "2026-02-20",
        "status": "healthy",
    },
]

# ──────────────────────────────────────────────────────────────
# SIMULATION LOGIC
# ──────────────────────────────────────────────────────────────

def mutate_highway(h):
    h["speed_kmh"] = round(random.uniform(10, 60), 1)
    h["congestion_pct"] = round(random.uniform(20, 95), 1)
    h["vehicle_count"] = random.randint(1500, 6000)
    # ORR spike: 20% chance of extreme congestion
    if h["id"] == "HWY-ORR-1" and random.random() < 0.20:
        h["congestion_pct"] = round(random.uniform(90, 99), 1)
        h["speed_kmh"] = round(random.uniform(5, 15), 1)
        h["vehicle_count"] = random.randint(5500, 7000)
    return h

def mutate_road(r):
    r["speed_kmh"] = round(random.uniform(10, 50), 1)
    r["congestion_pct"] = round(random.uniform(15, 90), 1)
    r["vehicle_count"] = random.randint(500, 3000)
    return r

def mutate_bridge(b):
    b["health_index"] = round(random.uniform(0.85, 1.0), 3)
    b["vibration_hz"] = round(random.uniform(2.0, 8.0), 1)
    b["load_tons"] = round(random.uniform(40, 130), 1)
    # Hebbal degradation: 12% chance of critical drop
    if b["id"] == "BR-HEBBAL-1" and random.random() < 0.12:
        b["health_index"] = round(random.uniform(0.55, 0.69), 3)
        b["vibration_hz"] = round(random.uniform(9.0, 14.0), 1)
        b["load_tons"] = round(random.uniform(120, 160), 1)
    # Silk Board stress: 8% chance
    if b["id"] == "BR-SILK-1" and random.random() < 0.08:
        b["health_index"] = round(random.uniform(0.60, 0.74), 3)
        b["vibration_hz"] = round(random.uniform(8.0, 12.0), 1)
    return b


def simulate():
    print("=" * 60)
    print("  Bangalore Smart Infrastructure Simulator v2.0")
    print("  Posting to:", API_URL)
    print("=" * 60)

    tick = 0
    while True:
        tick += 1
        highways = [mutate_highway(copy.deepcopy(h)) for h in HIGHWAYS]
        roads = [mutate_road(copy.deepcopy(r)) for r in ROADS]
        bridges = [mutate_bridge(copy.deepcopy(b)) for b in BRIDGES]

        payload = {
            "highways": highways,
            "roads": roads,
            "bridges": bridges,
        }

        try:
            resp = requests.post(API_URL, json=payload, timeout=5)
            result = resp.json()
            alerts = result.get("alerts_generated", 0)
            alert_str = f" | ⚠ {alerts} alerts" if alerts > 0 else ""
            print(f"[Tick {tick:04d}] Sent {len(highways)} hwys, {len(roads)} roads, {len(bridges)} bridges — HTTP {resp.status_code}{alert_str}")
        except requests.ConnectionError:
            print(f"[Tick {tick:04d}] ✗ Connection refused. Is the API running?")
        except Exception as e:
            print(f"[Tick {tick:04d}] ✗ Error: {e}")

        time.sleep(2)


if __name__ == "__main__":
    simulate()
