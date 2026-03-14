FUEL_PRICE_PER_L = 1.65
FUEL_KG_CO2_PER_L = 2.31

RIDESHARE_COST_PER_KM = 1.80
RIDESHARE_KG_CO2_PER_KM = 0.171

FASHION_AVG_ITEM_PRICE = 35.0
FASHION_KG_CO2_PER_ITEM = 33.0

STREAMING_MONTHLY_HRS = 45.0
STREAMING_KG_CO2_PER_HR = 0.036

GROCERY_KG_CO2_PER_USD = 0.45
AMAZON_LOGISTICS_KG_PER_USD = 0.12

TRANSPORT_FACTORS = [
    {"mode": "Walking", "min_speed": 0, "max_speed": 6, "factor": 0.0},
    {"mode": "Cycling", "min_speed": 6, "max_speed": 25, "factor": 0.005},
    {"mode": "Transit / e-bike", "min_speed": 25, "max_speed": 60, "factor": 0.089},
    {"mode": "Car", "min_speed": 60, "max_speed": 120, "factor": 0.171},
    {"mode": "Train / Highway", "min_speed": 120, "max_speed": float('inf'), "factor": 0.041},
]