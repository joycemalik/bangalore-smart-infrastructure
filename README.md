# Bangalore Smart Infrastructure Dashboard

A local-first, real-time IoT "Command Center" dashboard for monitoring Bangalore's critical infrastructure.

## 🚀 Overview

This application provides a live visualization of traffic density, bridge structural health, and vehicle speeds across four key locations in Bangalore:
1. **Silk Board Junction** (Traffic Density)
2. **Hebbal Flyover** (Bridge Structural Health)
3. **Electronic City Flyover** (Speed Metrics)
4. **Marathahalli ORR** (Traffic Density)

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python) - In-memory state management.
- **Simulator**: Python (Requests) - Real-time telemetric data generation.
- **Frontend**: HTML5, Tailwind CSS (Glassmorphism UI), Leaflet.js (Dark Mode Maps).

## 📂 Project Structure

- `api.py`: The "Brain". A REST API that handles telemetry ingestion and serves the current infrastructure status.
- `sim.py`: The "Sensors". A data simulator that posts randomized yet realistic telemetry data to the API every 2 seconds.
- `index.html`: The "Vision". A high-end, responsive dashboard that polls the API and updates the map and metrics dynamically.

## 🚦 How to Run

### 1. Start the API
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start the Sensor Simulation
```bash
python sim.py
```

### 3. Open the Dashboard
Simply open `index.html` in any modern web browser.

## 🚨 Features
- **Real-time Map**: Markers change color based on status (Green/Yellow/Red).
- **Glassmorphism UI**: High-end "Command Center" aesthetic with dark mode.
- **Dynamic Alerts**: Visual flashing alerts trigger when Hebbal Flyover bridge health drops below 80%.
- **Live Metrics**: Aggregated traffic and speed statistics.
