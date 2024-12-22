from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

class CustomerBase(BaseModel):
    name: str
    phone: str
    email: EmailStr
    is_active: bool = True

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class Customer(CustomerBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True