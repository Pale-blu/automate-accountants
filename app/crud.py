from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app import models, database
from datetime import datetime
from PyPDF2 import PdfReader
from pathlib import Path

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_receipt_file(file_name, file_path):
    db = next(get_db())
    existing = db.query(models.ReceiptFile).filter_by(file_name=file_name).first()
    if existing:
        existing.updated_at = datetime.utcnow()
        db.commit()
        return existing

    receipt_file = models.ReceiptFile(
        file_name=file_name,
        file_path=file_path,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(receipt_file)
    db.commit()
    db.refresh(receipt_file)
    return receipt_file

def validate_pdf(file_name):
    db = next(get_db())
    record = db.query(models.ReceiptFile).filter_by(file_name=file_name).first()
    if not record:
        return None

    try:
        PdfReader(record.file_path)
        record.is_valid = True
        record.invalid_reason = None
    except Exception as e:
        record.is_valid = False
        record.invalid_reason = str(e)

    record.updated_at = datetime.utcnow()
    db.commit()
    return record

def get_receipt_file(file_name):
    db = next(get_db())
    return db.query(models.ReceiptFile).filter_by(file_name=file_name).first()

def store_extracted_data(data: dict, file_path: str):
    db = next(get_db())
    receipt = models.Receipt(
    purchased_at=data.get("purchased_at"),
    merchant_name=data.get("merchant_name"),
    total_amount=data.get("total_amount"),
    file_path=file_path,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)
    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    return receipt

def mark_processed(file_name):
    db = next(get_db())
    record = db.query(models.ReceiptFile).filter_by(file_name=file_name).first()
    if record:
        record.is_processed = True
        record.updated_at = datetime.utcnow()
        db.commit()

def get_all_receipts():
    db = next(get_db())
    return db.query(models.Receipt).all()

def get_receipt_by_id(receipt_id: int):
    db = next(get_db())
    return db.query(models.Receipt).filter_by(id=receipt_id).first()
