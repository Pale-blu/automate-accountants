import os
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app import models, database
from datetime import datetime
from PyPDF2 import PdfReader
from pathlib import Path

RECEIPT_YEARS = [str(year) for year in range(2018, 2026)]

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



# List of folders to check
def validate_pdf(file_name: str, db: Session):
    record = db.query(models.ReceiptFile).filter_by(file_name=file_name).first()
    if not record:
        return None

    from pathlib import Path
    from PyPDF2 import PdfReader
    from datetime import datetime

    RECEIPT_YEARS = [str(year) for year in range(2018, 2026)]
    base_dir = Path(".")
    actual_path = None

    for year in RECEIPT_YEARS:
        year_folder = base_dir / year
        if year_folder.exists() and year_folder.is_dir():
            for path in year_folder.rglob(file_name):
                if path.is_file():
                    actual_path = path
                    break
        if actual_path:
            break

    if not actual_path:
        record.is_valid = False
        record.invalid_reason = "File not found in any year folder or subfolder"
    else:
        try:
            PdfReader(str(actual_path))
            record.is_valid = True
            record.invalid_reason = None
            record.file_path = str(actual_path)
        except Exception as e:
            record.is_valid = False
            record.invalid_reason = str(e)

    record.updated_at = datetime.utcnow()
    db.add(record)
    db.commit()
    db.refresh(record)  # ✅ Guarantees object is still attached
    return record

    # Try reading the PDF
    try:
        PdfReader(str(actual_path))
        record.is_valid = True
        record.invalid_reason = None
        record.file_path = str(actual_path)
    except Exception as e:
        record.is_valid = False
        record.invalid_reason = str(e)

    record.updated_at = datetime.utcnow()
    db.commit()
    return record

def get_receipt_file(file_name: str, db: Session):
    return db.query(models.ReceiptFile).filter_by(file_name=file_name).first()

def store_extracted_data(data: dict, file_path: str, db: Session):
    from datetime import datetime
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


def mark_processed(file_name: str, db: Session):
    from datetime import datetime
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
