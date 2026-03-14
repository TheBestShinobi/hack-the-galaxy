from pydantic import BaseModel

class ParseResult(BaseModel):
    merchant: str
    category: str
    co2_kg: float
    confidence: float
    needs_review: bool
    explanation: str