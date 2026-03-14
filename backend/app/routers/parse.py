from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.services.bank_parser import BankParser
from app.models.parse_result import ParseResult

router = APIRouter(prefix="/parse", tags=["parsing"])
parser = BankParser()

class BankStatementRequest(BaseModel):
    data: str

@router.post("/bank", response_model=List[ParseResult])
async def parse_bank_statement(request: BankStatementRequest):
    try:
        results = parser.parse_input(request.data)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse statement: {str(e)}")