from typing import Optional
from core.security import verify_password, create_access_token
from schemas.user import UserLogin

# Hardcoded "Database"
FAKE_USER_DB = {
    "admin": {
        "id": 1,
        "username": "jaja",
        "full_name": "John Doe Surveyor",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$7kP.K6G06UvYw.v7tXN3Se6nI6yZ9vLzS8R4iX.O/2/29P5g7B2m2", # hash for 'jaja', # hash for 'jakarta'  # hash for 'password123'
        "is_active": True,
    }
}

def authenticate_user(login_data: UserLogin) -> Optional[dict]:
    user = FAKE_USER_DB.get(login_data.username)
    if not user:
        return None
    if not verify_password(login_data.password, user["hashed_password"]):
        return None
    return user
