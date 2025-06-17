# receipt_processor/app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import os
from datetime import datetime

from app import database, models, crud, ocr_utils
from app.schemas import ReceiptFileSchema, ReceiptSchema

# Initialize the database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_UPLOAD_DIR = Path(".")
UPLOAD_YEAR = str(datetime.now().year)
UPLOAD_DIR = BASE_UPLOAD_DIR / UPLOAD_YEAR
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    filepath = UPLOAD_DIR / file.filename
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_file = crud.create_receipt_file(file.filename, str(filepath))
    return {"message": "File uploaded successfully", "file": db_file}

@app.post("/validate")
def validate_file(file_name: str):
    result = crud.validate_pdf(file_name)
    if result is None:
        raise HTTPException(status_code=404, detail="File not found")
    return result

@app.post("/process")
def process_file(file_name: str):
    receipt_file = crud.get_receipt_file(file_name)
    if not receipt_file:
        raise HTTPException(status_code=404, detail="File not found")
    if not receipt_file.is_valid:
        raise HTTPException(status_code=400, detail="File is not valid")

    extracted = ocr_utils.extract_receipt_data(receipt_file.file_path)
    receipt = crud.store_extracted_data(extracted, receipt_file.file_path)
    crud.mark_processed(file_name)
    return receipt

@app.get("/receipts")
def list_receipts():
    return crud.get_all_receipts()

@app.get("/receipts/{receipt_id}")
def get_receipt(receipt_id: int):
    receipt = crud.get_receipt_by_id(receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt