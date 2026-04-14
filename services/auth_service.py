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
        "hashed_password": "$2b$12$R9P6L9XzG0k7.N/6U0vHVuM1T8Y8m9Wp1jK4R7fGvH2mN5s3a4b5c", # hash for 'jakarta'  # hash for 'password123'
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
