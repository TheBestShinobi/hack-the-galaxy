from typing import Dict, Any, List
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

def calculate_total_from_items(items: List[Dict[str, Any]]) -> float:
    """Calculates total kg CO2 from a list of parsed items."""
    if not items:
        return 0.0
    return round(sum(float(item.get("kg_co2", 0)) for item in items), 3)

def get_emission_rating(kg_co2: float, item_count: int = 1) -> str:
    """Returns a rating based on average CO2 intensity per item."""
    count = max(1, item_count)
    avg_per_item = kg_co2 / count

    # Thresholds: <1kg/item (Groceries), 1-5kg/item (Mixed), >5kg/item (High Impact/Fuel)
    if avg_per_item <= 1.0:
        return "Low Intensity (Good)"
    elif avg_per_item <= 5.0:
        return "Moderate Intensity"
    else:
        return "High Intensity"