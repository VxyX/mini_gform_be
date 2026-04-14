from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Optional[dict] = None  # Re-including user data in the token response as requested

class TokenPayload(BaseModel):
    sub: Optional[int] = None
