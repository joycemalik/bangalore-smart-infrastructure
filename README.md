# 🏙️ Bangalore Smart Infrastructure Dashboard v2.0
### Advanced Command & Control | Real-Time IoT Traffic & Structural Management

A high-density, interactive tactical dashboard designed to monitor and manage Bangalore's critical infrastructure. This system provides a unified view of highway congestion, arterial road speed, and bridge structural health through real-time telemetry and a "glassmorphism" command center interface.

---

## 🏗️ System Architecture: The Three Pillars

The application is built on a "local-first" micro-architecture consisting of three core modules:

### 1. 📡 The Physical Layer (`sim.py`)
A robust telemetry generator that simulates a network of **11 critical infrastructure assets**:
- **3 Highways**: Using coordinate paths (Polylines) to track speed, congestion, and vehicle volume.
- **4 Arterial Roads**: High-density urban corridors with dynamic traffic mutation.
- **4 Strategic Bridges**: Point-based sensors monitoring Health Index (0-1.0), Vibration (Hz), and Structural Load (Tons).
- **Chaos Engine**: Randomly injects critical events, such as 99% congestion spikes on the ORR or structural health drops below 70% on the Hebbal Flyover.

### 2. 🧠 The Logic Layer (`api.py`)
A FastAPI-powered REST backend that serves as the system's "Brain":
- **State Management**: Maintains an in-memory high-fidelity state of every node in the network.
- **Bulk Telemetry Ingestion**: Processes mass up-link data from the simulation layer every 2 seconds.
- **Automated Alert Generation**: Categorizes events into "Normal", "Warning", and "Critical" based on predefined logic thresholds.
- **Interactive Action Controller**: An endpoint that receives remote commands from the UI, allowing operators to "Dispatch Patrols" or "Adjust Signal Timing," which immediately impacts the live state.

### 3. 🖥️ The Presentation Layer (`index.html`)
A triple-panel high-end Tactical Dashboard:
- **Left Panel (Global Status)**: Real-time network-wide metrics, a Live Alert Feed, and a searchable/clickable Network Overview.
- **Center Panel (Tactical Map)**: A Leaflet.js-based Dark Mode map rendering:
    - **Thick Polylines**: For Highways, color-coded by speed (Green > 40km/h, Yellow 20-40, Red < 20).
    - **Dashed Polylines**: For congested arterial roads.
    - **Pulsing Markers**: Bridges that pulse red during structural warning states.
- **Right Panel (Node Inspector)**: A hidden-by-default console that slides out when an asset is clicked. It displays granular metrics (vibration, load, congestion %) and provides interactive action buttons.

---

## ⚡ Key Features

- **High-Density Mapping**: Visualizes stretches of road rather than simple points, providing a more realistic spatial view.
- **Real-Time Polling**: The UI syncs with the API every 2,000ms, ensuring zero stale data.
- **Bi-Directional Interaction**: Don't just watch the map—interact with it. Operators can take corrective actions directly from the Node Inspector.
- **Structural Health Monitoring (SHM)**: Dedicated bridge monitoring including vibration frequency and load stress.
- **Glassmorphism Aesthetic**: Modern, dark-mode CSS with backdrop filters, designed for pro-grade monitoring stations.
- **Robust Error Handling**: Auto-reconnect logic for UI fetching if the backend restarts.

---

## 📍 Monitored Assets

| Asset Type | Primary Locations |
| :--- | :--- |
| **Highways** | ORR Stretch, Hosur Road Elevated, Airport Road (Hebbal-Yelahanka) |
| **Arterial Roads** | MG Road, Indiranagar 100ft, Koramangala 80ft, Tumkur Road |
| **Bridges** | Hebbal Flyover, Silk Board Flyover, KR Puram Bridge, Nayandahalli Junction |

---

## 🚀 Installation & Launch

### 1. Prerequisites
Ensure you have Python 3.8+ installed.
```bash
pip install fastapi uvicorn requests
```

### 2. Start the Backend (The Brain)
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Start the Simulation (The Sensors)
In a new terminal:
```bash
python sim.py
```

### 4. Open the Interface
Simply open `index.html` in your browser.

---

## 🕹️ Usage Guide

1. **Monitor the Alerts**: Keep an eye on the Left Panel. If an alert appears, click the node name in the Network Overview to locate it.
2. **Tactical Inspection**: Click on any Road or Bridge on the map. The **Right Panel** will slide out with live telemetry.
3. **Execute Actions**: If a road is "Critical" (Red), use the **"Dispatch Patrol"** button to manually reduce congestion and restore flow.
4. **Bridge Management**: If a bridge vibrates at > 8Hz, use **"Adjust Signal Timing"** or **"Dispatch"** to stabilize the structure.
5. **Close Inspector**: Use the `X` button in the Right Panel to return to the full-screen map view.
