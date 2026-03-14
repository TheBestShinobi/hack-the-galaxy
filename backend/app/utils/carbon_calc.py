from typing import Dict, Any
from app.data import emission_factors as ef

def calculate_transport_emissions(speed_kmh: float, distance_km: float) -> Dict[str, Any]:
    speed = max(0.0, speed_kmh)
    
    for entry in ef.TRANSPORT_FACTORS:
        if entry["min_speed"] <= speed < entry["max_speed"]:
            emissions = distance_km * entry["factor"]
            return {
                "mode": entry["mode"],
                "emissions_kg": round(emissions, 4),
                "factor_used": entry["factor"]
            }
            
    return {
        "mode": "Unknown",
        "emissions_kg": 0.0,
        "factor_used": 0.0
    }