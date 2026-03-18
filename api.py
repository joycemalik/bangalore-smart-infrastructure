from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────────────────────
# DATA MODELS
# ──────────────────────────────────────────────────────────────

class HighwayData(BaseModel):
    id: str
    name: str
    path: List[List[float]]
    speed_kmh: float
    congestion_pct: float
    lanes: int
    status: str  # "normal", "congested", "critical"
    vehicle_count: int

class RoadData(BaseModel):
    id: str
    name: str
    path: List[List[float]]
    speed_kmh: float
    congestion_pct: float
    lanes: int
    status: str
    vehicle_count: int

class BridgeData(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    health_index: float
    vibration_hz: float
    load_tons: float
    last_inspection: str
    status: str  # "healthy", "warning", "critical"

class BulkUpdate(BaseModel):
    highways: Optional[List[HighwayData]] = None
    roads: Optional[List[RoadData]] = None
    bridges: Optional[List[BridgeData]] = None

class ActionPayload(BaseModel):
    action: str
    node_id: str

# ──────────────────────────────────────────────────────────────
# GLOBAL STATE
# ──────────────────────────────────────────────────────────────

state = {
    "highways": {},
    "roads": {},
    "bridges": {},
    "alerts": [],
    "actions_log": [],
}

# ──────────────────────────────────────────────────────────────
# ENDPOINTS
# ──────────────────────────────────────────────────────────────

@app.get("/state")
async def get_state():
    return {
        "highways": list(state["highways"].values()),
        "roads": list(state["roads"].values()),
        "bridges": list(state["bridges"].values()),
        "alerts": state["alerts"][-30:],  # last 30 alerts
        "actions_log": state["actions_log"][-20:],
        "timestamp": time.time(),
    }


@app.post("/update")
async def bulk_update(data: BulkUpdate):
    alerts = []

    if data.highways:
        for h in data.highways:
            d = h.model_dump()
            # Auto-derive status
            if h.congestion_pct > 85:
                d["status"] = "critical"
                alerts.append({
                    "ts": time.time(),
                    "severity": "critical",
                    "node_id": h.id,
                    "message": f"CRITICAL: {h.name} congestion at {h.congestion_pct:.0f}%"
                })
            elif h.congestion_pct > 60:
                d["status"] = "congested"
                alerts.append({
                    "ts": time.time(),
                    "severity": "warning",
                    "node_id": h.id,
                    "message": f"WARNING: {h.name} congestion rising to {h.congestion_pct:.0f}%"
                })
            else:
                d["status"] = "normal"
            state["highways"][h.id] = d

    if data.roads:
        for r in data.roads:
            d = r.model_dump()
            if r.congestion_pct > 80:
                d["status"] = "critical"
                alerts.append({
                    "ts": time.time(),
                    "severity": "critical",
                    "node_id": r.id,
                    "message": f"CRITICAL: {r.name} congestion at {r.congestion_pct:.0f}%"
                })
            elif r.congestion_pct > 55:
                d["status"] = "congested"
            else:
                d["status"] = "normal"
            state["roads"][r.id] = d

    if data.bridges:
        for b in data.bridges:
            d = b.model_dump()
            if b.health_index < 0.7:
                d["status"] = "critical"
                alerts.append({
                    "ts": time.time(),
                    "severity": "critical",
                    "node_id": b.id,
                    "message": f"CRITICAL: {b.name} structural health at {b.health_index*100:.0f}%! Vibration: {b.vibration_hz:.1f}Hz"
                })
            elif b.health_index < 0.85:
                d["status"] = "warning"
                alerts.append({
                    "ts": time.time(),
                    "severity": "warning",
                    "node_id": b.id,
                    "message": f"WARNING: {b.name} health degrading — {b.health_index*100:.0f}%"
                })
            else:
                d["status"] = "healthy"
            state["bridges"][b.id] = d

    state["alerts"].extend(alerts)
    # Keep only last 100 alerts
    if len(state["alerts"]) > 100:
        state["alerts"] = state["alerts"][-100:]

    return {"status": "ok", "alerts_generated": len(alerts)}


@app.post("/action/{node_id}")
async def perform_action(node_id: str, payload: ActionPayload):
    action = payload.action
    log_entry = {
        "ts": time.time(),
        "node_id": node_id,
        "action": action,
        "result": "dispatched"
    }

    # Find and modify node state
    found = False
    for category in ["highways", "roads"]:
        if node_id in state[category]:
            node = state[category][node_id]
            if action == "dispatch_patrol":
                node["congestion_pct"] = max(10, node["congestion_pct"] - 25)
                node["speed_kmh"] = min(60, node["speed_kmh"] + 15)
                node["status"] = "normal"
                log_entry["result"] = f"Patrol dispatched. Congestion reduced to {node['congestion_pct']:.0f}%"
            elif action == "adjust_signal":
                node["congestion_pct"] = max(15, node["congestion_pct"] - 15)
                node["speed_kmh"] = min(55, node["speed_kmh"] + 10)
                log_entry["result"] = f"Signals re-phased. Speed improved to {node['speed_kmh']:.0f} km/h"
            found = True
            break

    if node_id in state["bridges"]:
        bridge = state["bridges"][node_id]
        if action == "dispatch_patrol":
            bridge["status"] = "healthy"
            bridge["health_index"] = 0.95
            bridge["vibration_hz"] = max(2.0, bridge["vibration_hz"] - 3)
            log_entry["result"] = f"Inspection team dispatched. Bridge stabilized."
        elif action == "adjust_signal":
            bridge["load_tons"] = max(10, bridge["load_tons"] - 20)
            log_entry["result"] = f"Load diversion activated. Load reduced to {bridge['load_tons']:.0f}T"
        found = True

    if not found:
        log_entry["result"] = "Node not found"

    state["actions_log"].append(log_entry)
    return log_entry
