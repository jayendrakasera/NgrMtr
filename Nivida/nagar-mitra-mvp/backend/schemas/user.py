from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    mobile_number: str
    name: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('mobile_number')
    def validate_mobile_number(cls, v):
        # Simple mobile number validation
        if not v.startswith('+91') or len(v) != 13:
            raise ValueError('Mobile number must start with +91 and be 13 characters long')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserLogin(BaseModel):
    mobile_number: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None