from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.receipt_parser import parse_receipt, parse_receipt_image
from app.services.bank_parser import parse_bank

router = APIRouter(prefix="/parse", tags=["parse"])


class TextInput(BaseModel):
    text: str

@router.post("/receipt/image")
async def receipt_image(
    file: UploadFile = File(...),
):
    try:
        image_bytes = await file.read()
        return await parse_receipt_image(image_bytes, file.content_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse receipt image: {str(e)}")

@router.post("/receipt")
async def receipt_text(body: TextInput):
    return await parse_receipt(body.text)

@router.post("/bank")
async def bank(body: TextInput):
    return await parse_bank(body.text)
