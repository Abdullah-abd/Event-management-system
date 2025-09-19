from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date, time
from pydantic.utils import GetterDict

# ----------------------
# User Schemas
# ----------------------

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


# ----------------------
# Token Schemas
# ----------------------

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


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    # Image handled via UploadFile in route


class EventGetter(GetterDict):
    def get(self, key, default=None):
        if key == "image":
            return getattr(self._obj, "image", None)  # ✅ fixed to match DB
        return getattr(self._obj, key, default)


class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    date: date
    time: time
    image_url: Optional[str] = None  # ✅ frontend will receive this field
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        getter_dict = EventGetter
