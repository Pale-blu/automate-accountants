import pytesseract
from pdf2image import convert_from_path
from datetime import datetime
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_receipt_data(pdf_path: str):
    images = convert_from_path(
        pdf_path,
        poppler_path=r"C:\Program Files\poppler\poppler-24.08.0\Library\bin"  # Update path as needed
    )    
    text = "\n".join(pytesseract.image_to_string(img) for img in images)

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Try to guess merchant from top lines
    merchant = "Unknown"
    for line in lines[:10]:  # first 10 non-empty lines
        if re.search(r"[a-zA-Z]{4,}", line) and not any(x in line.lower() for x in ["thank", "receipt", "total", "item"]):
            merchant = line
            break

    # Extract purchase date and time
    date_match = re.search(r"(\d{2}/\d{2}/\d{4})\s+(\d{2}[:\.]\d{2})", text)
    total_match = re.search(r"Total\s*[:\$]?\s*(\d+\.\d{2})", text)

    try:
        purchased_at = datetime.strptime(
            f"{date_match[1]} {date_match[2].replace('.', ':')}",
            "%m/%d/%Y %H:%M"
        ) if date_match else None
    except:
        purchased_at = None

    total = float(total_match[1]) if total_match else 0.0

    return {
        "merchant_name": merchant,
        "purchased_at": purchased_at,
        "total_amount": total
    }
