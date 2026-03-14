from .gemini import ask_gemini_json

_PROMPT = """\
You are a carbon footprint calculator.
Given receipt text, identify each line item and estimate its kg CO2e.
Classify each item into: food, transport, energy, shopping, digital, or other.
Use IPCC/DEFRA 2024 emission factors.

Return ONLY valid JSON in this exact shape — no extra text, no markdown:
{
  "items": [
    {
      "description": "Beef mince 500g",
      "category": "food",
      "kg_co2": 13.5,
      "confidence": "high"
    }
  ],
  "total_kg_co2": 13.5
}

confidence must be: high | medium | low

Receipt text:
"""


async def parse_receipt(text: str) -> dict:
    result = await ask_gemini_json(_PROMPT + text)
    result["source"] = "receipt"
    if "items" in result:
        result["total_kg_co2"] = round(
            sum(i.get("kg_co2", 0) for i in result["items"]), 3
        )
    return result