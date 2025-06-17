from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FileRequest(BaseModel):
    file_name: str

class ReceiptFileSchema(BaseModel):
    id: int
    file_name: str
    file_path: str
    is_valid: bool
    invalid_reason: Optional[str]
    is_processed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ReceiptSchema(BaseModel):
    id: int
    purchased_at: Optional[datetime]
    merchant_name: str
    total_amount: float
    file_path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
