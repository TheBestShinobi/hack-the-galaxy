from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.carbon_calc import calculate_transport_emissions

router = APIRouter(prefix="/log", tags=["logging"])

class MovementLogRequest(BaseModel):
    distance_km: float
    speed_kmh: float

class MovementLogResponse(BaseModel):
    mode: str
    emissions_kg: float
    factor_used: float

@router.post("/movement", response_model=MovementLogResponse)
async def log_movement(log: MovementLogRequest):
    result = calculate_transport_emissions(log.speed_kmh, log.distance_km)
    
    return result