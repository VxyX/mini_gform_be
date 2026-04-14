from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    email: Optional[EmailStr] = None
    is_active: bool = True

    class Config:
        from_attributes = True
