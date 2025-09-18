from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from datetime import date, time 
# ✅ User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "normal"  # default to normal user

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True

# ✅ Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
# ----------------------
# Event Schemas
# ----------------------

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    time: time
    image_url: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    image_url: Optional[str] = None


class EventResponse(EventBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # ⚡ Pydantic v2 support for ORM models
