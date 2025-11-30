import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database import get_db
from models import Reading

# --- 1. Pydantic Models (Data Schemas) ---
# These models define the *exact* structure of your JSON responses.
# FastAPI uses them to validate your data and auto-generate documentation.

# Sub-model for 'sensors' in latest_response.json
class SensorData(BaseModel):
    ec: float
    ph: float
    temp_c: float

# Sub-model for 'predictions' in latest_response.json
class PredictionData(BaseModel):
    n_ppm: float
    p_ppm: float
    k_ppm: float

# Define allowed status values using an Enum for robustness
class NutrientStatus(str, Enum):
    ok = "ok"
    low = "low"
    high = "high"

class OverallStatus(str, Enum):
    ok = "ok"
    warning = "warning"
    danger = "danger"

# Sub-model for 'status' in latest_response.json
class StatusData(BaseModel):
    n_status: NutrientStatus
    p_status: NutrientStatus
    k_status: NutrientStatus
    overall_status: OverallStatus

# Main model for latest_response.json
class LatestReadingResponse(BaseModel):
    timestamp: datetime
    plant_id: str
    lettuce_image_url: str
    sensors: SensorData
    predictions: PredictionData
    status: StatusData
    recommendation: str

# Model for one data point in history_response.json
class HistoryDataPoint(BaseModel):
    timestamp: datetime
    n_ppm: float
    p_ppm: float
    k_ppm: float
    ec: float
    ph: float

# Main model for history_response.json
class HistoryResponse(BaseModel):
    query_range: str
    data_points: List[HistoryDataPoint]

# Input model for creating a new reading
class ReadingCreate(BaseModel):
    timestamp: datetime
    plant_id: str
    lettuce_image_url: str
    # Sensors
    ec: float
    ph: float
    temp_c: float
    # Predictions
    n_ppm: float
    p_ppm: float
    k_ppm: float

# --- 2. FastAPI App Instance ---
app = FastAPI(
    title="LEAFCLOUD API",
    description="API for the LEAFCLOUD Hydroponics Monitoring System.",
    version="1.0.0"
)

# --- 3. API Endpoints ---
@app.post(
    "/api/v1/readings",
    response_model=ReadingCreate,
    summary="Add a New Sensor Reading"
)
async def create_reading(reading: ReadingCreate, db: Session = Depends(get_db)):
    """
    Ingests a new sensor reading and saves it to the database.
    """
    db_reading = Reading(
        timestamp=reading.timestamp,
        plant_id=reading.plant_id,
        lettuce_image_url=reading.lettuce_image_url,
        ec=reading.ec,
        ph=reading.ph,
        temp_c=reading.temp_c,
        n_ppm=reading.n_ppm,
        p_ppm=reading.p_ppm,
        k_ppm=reading.k_ppm
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return reading

@app.get(
    "/api/v1/readings/latest",
    response_model=LatestReadingResponse,
    summary="Get Latest Sensor Reading"
)
async def get_latest_reading(db: Session = Depends(get_db)):
    """
    Retrieves the single most recent reading from the hydroponics system.
    This provides all data needed for the main dashboard.
    """
    latest_reading = db.query(Reading).order_by(desc(Reading.timestamp)).first()

    if not latest_reading:
        raise HTTPException(status_code=404, detail="No readings found")

    # Determine status (Mock logic for now - ideally this comes from a utility or config)
    def get_status(value, optimal):
        if value < optimal * 0.9: return NutrientStatus.low
        if value > optimal * 1.1: return NutrientStatus.high
        return NutrientStatus.ok

    # Optimal values (example)
    n_status = get_status(latest_reading.n_ppm, 150.0)
    p_status = get_status(latest_reading.p_ppm, 50.0)
    k_status = get_status(latest_reading.k_ppm, 200.0)
    
    overall_status = OverallStatus.ok
    if any(s != NutrientStatus.ok for s in [n_status, p_status, k_status]):
        overall_status = OverallStatus.warning
        # Simple logic: if any are way off, danger (omitted for brevity)

    return {
        "timestamp": latest_reading.timestamp,
        "plant_id": latest_reading.plant_id,
        "lettuce_image_url": latest_reading.lettuce_image_url,
        "sensors": {
            "ec": latest_reading.ec,
            "ph": latest_reading.ph,
            "temp_c": latest_reading.temp_c
        },
        "predictions": {
            "n_ppm": latest_reading.n_ppm,
            "p_ppm": latest_reading.p_ppm,
            "k_ppm": latest_reading.k_ppm
        },
        "status": {
            "n_status": n_status,
            "p_status": p_status,
            "k_status": k_status,
            "overall_status": overall_status
        },
        "recommendation": "System is running optimally." if overall_status == OverallStatus.ok else "Check nutrient levels."
    }

@app.get(
    "/api/v1/readings/history",
    response_model=HistoryResponse,
    summary="Get Historical Sensor Readings"
)
async def get_history(range: str = "7d", db: Session = Depends(get_db)):
    """
    Retrieves a list of historical readings for a specified time range.
    Used to populate charts in the app.
    
    Query Parameters:
    - **range**: The time range (e.g., '24h', '7d', '30d').
    """
    
    # Calculate cutoff time
    now = datetime.utcnow()
    if range == "24h":
        cutoff = now - timedelta(hours=24)
    elif range == "7d":
        cutoff = now - timedelta(days=7)
    elif range == "30d":
        cutoff = now - timedelta(days=30)
    else:
        # Default to 7d if invalid or unspecified
        cutoff = now - timedelta(days=7)

    readings = db.query(Reading).filter(Reading.timestamp >= cutoff).order_by(Reading.timestamp.asc()).all()

    data_points = []
    for r in readings:
        data_points.append({
            "timestamp": r.timestamp,
            "n_ppm": r.n_ppm,
            "p_ppm": r.p_ppm,
            "k_ppm": r.k_ppm,
            "ec": r.ec,
            "ph": r.ph
        })

    return {
        "query_range": range,
        "data_points": data_points
    }

# This is for running the file directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)