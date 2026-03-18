from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TelemetryData(BaseModel):
    location: str
    type: str # 'traffic', 'bridge', or 'speed'
    value: float
    lat: float
    lng: float

# Global dictionary to hold the state
state = {}

@app.post("/telemetry")
async def update_telemetry(data: TelemetryData):
    state[data.location] = {
        "location": data.location,
        "type": data.type,
        "value": data.value,
        "lat": data.lat,
        "lng": data.lng
    }
    return {"status": "success"}

@app.get("/status")
async def get_status():
    return list(state.values())

