from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="SentinelAI", version="0.1.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def home():
    return FileResponse("app/static/index.html")


class GPSPoint(BaseModel):
    lat: float
    lon: float
    ts: datetime


class DeviceMeta(BaseModel):
    device_id: str
    os: str
    model: Optional[str] = None
    emulator: bool = False


class SensorSample(BaseModel):
    accel: float
    gyro: float
    ts: datetime


class ClaimRequest(BaseModel):
    claim_id: str
    user_id: str
    gps: List[GPSPoint]
    device: DeviceMeta
    sensors: List[SensorSample] = Field(default_factory=list)
    weather: Optional[str] = None


class RiskResponse(BaseModel):
    claim_id: str
    risk_score: float
    risk_band: str
    factors: dict


def _trajectory_anomaly(gps: List[GPSPoint]) -> float:
    if len(gps) < 2:
        return 0.1
    # Simple heuristic: large jumps in short time = anomaly
    jumps = 0
    for i in range(1, len(gps)):
        dt = (gps[i].ts - gps[i - 1].ts).total_seconds()
        dist = ((gps[i].lat - gps[i - 1].lat) ** 2 + (gps[i].lon - gps[i - 1].lon) ** 2) ** 0.5
        if dt > 0 and dist / dt > 0.01:
            jumps += 1
    return min(1.0, jumps / max(1, len(gps) - 1))


def _behavior_deviation(sensors: List[SensorSample]) -> float:
    if not sensors:
        return 0.2
    spikes = sum(1 for s in sensors if abs(s.accel) > 20 or abs(s.gyro) > 10)
    return min(1.0, spikes / max(1, len(sensors)))


def _device_network_risk(device: DeviceMeta) -> float:
    return 0.8 if device.emulator else 0.2


def _risk_score(a: float, b: float, c: float) -> float:
    w1, w2, w3 = 0.45, 0.35, 0.20
    return round(w1 * a + w2 * b + w3 * c, 4)


def _risk_band(score: float) -> str:
    if score < 0.35:
        return "low"
    if score < 0.7:
        return "medium"
    return "high"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/claims/score", response_model=RiskResponse)
def score_claim(payload: ClaimRequest):
    a = _trajectory_anomaly(payload.gps)
    b = _behavior_deviation(payload.sensors)
    c = _device_network_risk(payload.device)
    score = _risk_score(a, b, c)
    band = _risk_band(score)

    return RiskResponse(
        claim_id=payload.claim_id,
        risk_score=score,
        risk_band=band,
        factors={
            "trajectory_anomaly": a,
            "behavior_deviation": b,
            "device_network_risk": c,
        },
    )
