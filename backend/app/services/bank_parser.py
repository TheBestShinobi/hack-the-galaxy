import csv
import re
import io
import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from app.data import emission_factors as ef

@dataclass
class CarbonEstimate:
    category: str
    emissions_kg: float
    confidence: float
    note: str
    needs_review: bool

class BankParser:
    def __init__(self):
        self.rules = [
            {"re": re.compile(r"SHELL|BP|ESSO|EXXON|CHEVRON|TOTAL", re.I), "cat": "Fuel", "fn": self._calc_fuel, "conf": 0.95},
            {"re": re.compile(r"UBER|LYFT|BOLT|FREENOW", re.I), "cat": "Rideshare", "fn": self._calc_rideshare, "conf": 0.90},
            {"re": re.compile(r"WHOLE FOODS|TESCO|SAINSBURY|KROGER|WAITROSE|ALDI|LIDL|SAFEWAY", re.I), "cat": "Groceries", "fn": self._calc_groceries, "conf": 0.85},
            {"re": re.compile(r"H&M|ZARA|UNIQLO|PRIMARK|ASOS|SHEIN", re.I), "cat": "Fast Fashion", "fn": self._calc_fashion, "conf": 0.90},
            {"re": re.compile(r"NETFLIX|YOUTUBE|DISNEY|SPOTIFY|HULU", re.I), "cat": "Streaming", "fn": self._calc_streaming, "conf": 0.95},
            {"re": re.compile(r"AMAZON|AMZN|MARKETPLACE", re.I), "cat": "E-commerce", "fn": self._calc_amazon, "conf": 0.80},
        ]

    def _calc_fuel(self, amount: float) -> float:
        liters = amount / ef.FUEL_PRICE_PER_L
        return liters * ef.FUEL_KG_CO2_PER_L

    def _calc_rideshare(self, amount: float) -> float:
        km = amount / ef.RIDESHARE_COST_PER_KM
        return km * ef.RIDESHARE_KG_CO2_PER_KM

    def _calc_groceries(self, amount: float) -> float:
        return amount * ef.GROCERY_KG_CO2_PER_USD

    def _calc_fashion(self, amount: float) -> float:
        items = max(1.0, amount / ef.FASHION_AVG_ITEM_PRICE)
        return items * ef.FASHION_KG_CO2_PER_ITEM

    def _calc_streaming(self, amount: float) -> float:
        return ef.STREAMING_MONTHLY_HRS * ef.STREAMING_KG_CO2_PER_HR

    def _calc_amazon(self, amount: float) -> float:
        return amount * ef.AMAZON_LOGISTICS_KG_PER_USD

    def classify_transaction(self, description: str, amount: float) -> CarbonEstimate:
        amount = abs(float(amount))

        for rule in self.rules:
            if rule["re"].search(description):
                emissions = rule["fn"](amount)
                return CarbonEstimate(
                    category=rule["cat"],
                    emissions_kg=round(emissions, 2),
                    confidence=rule["conf"],
                    note=f"Matched via {rule['cat']} model",
                    needs_review=False
                )

        # Fallback for unknown items
        return CarbonEstimate(
            category="Other/Unknown",
            emissions_kg=0.0,
            confidence=0.1,
            note="Unrecognized merchant",
            needs_review=True
        )

    def parse_input(self, data: str) -> List[Dict[str, Any]]:
        """Handles both CSV data and plain text line-by-line."""
        results = []
        
        if "," in data:
            f = io.StringIO(data.strip())
            reader = csv.DictReader(f)
            for row in reader:
                # Flexible header detection
                desc = row.get('Description') or row.get('Merchant') or row.get('Name') or ""
                amt = row.get('Amount') or row.get('Value') or 0
                if desc and amt:
                    estimate = self.classify_transaction(desc, amt)
                    results.append(self._format_output(row, estimate))
            if results: return results

        for line in data.split('\n'):
            if not line.strip(): continue
            match = re.search(r"([\d,]+\.\d{2})", line)
            if match:
                amt = float(match.group(1).replace(',', ''))
                desc = line.replace(match.group(1), "").strip()
                estimate = self.classify_transaction(desc, amt)
                results.append(self._format_output({"raw": line}, estimate))
        
        return results

    def _format_output(self, original: Dict, est: CarbonEstimate) -> Dict:
        return {
            "merchant": original.get('Description', original.get('raw', 'Unknown')),
            "category": est.category,
            "co2_kg": est.emissions_kg,
            "confidence": est.confidence,
            "needs_review": est.needs_review,
            "explanation": est.note
        }

if __name__ == "__main__":
    parser = BankParser()
    sample_data = """Description,Amount
Shell Service Station,55.00
Uber Trip,22.40
Netflix.com,15.99
Whole Foods Market,104.20
H&M Online,78.00
Amazon.com,45.12
Local Coffee Shop,4.50"""

    report = parser.parse_input(sample_data)
    for entry in report:
        status = "[!]" if entry['needs_review'] else "[OK]"
        print(f"{status} {entry['merchant'][:20]:<20} | {entry['category']:<12} | {entry['co2_kg']} kg CO2")