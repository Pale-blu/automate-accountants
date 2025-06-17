# receipt_processor/app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import os
from datetime import datetime
from fastapi import Query
from app import models, database
from app.schemas import ReceiptFileSchema, ReceiptSchema, FileRequest
from fastapi import Body
from app import crud
from app.database import get_db
from sqlalchemy.orm import Session
from app import ocr_utils

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

RECEIPT_YEARS = [str(year) for year in range(2018, 2026)]

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    filepath = UPLOAD_DIR / file.filename
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_file = crud.create_receipt_file(file.filename, str(filepath))
    return {"message": "File uploaded successfully", "file": db_file}



@app.post("/validate", response_model=ReceiptFileSchema)
def validate_file(data: FileRequest, db: Session = Depends(get_db)):
    result = crud.validate_pdf(data.file_name, db)
    if result is None:
        raise HTTPException(status_code=404, detail="File not found in database")
    return result

@app.post("/process", response_model=ReceiptSchema)
def process_file(data: FileRequest, db: Session = Depends(get_db)):
    file_name = data.file_name
    receipt_file = crud.get_receipt_file(file_name, db)
    if not receipt_file:
        raise HTTPException(status_code=404, detail="File not found in database")
    if not receipt_file.is_valid:
        raise HTTPException(status_code=400, detail="File is not valid")

    extracted = ocr_utils.extract_receipt_data(receipt_file.file_path)
    receipt = crud.store_extracted_data(extracted, receipt_file.file_path, db)
    crud.mark_processed(file_name, db)
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