from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from surveyor_backend.core.config import settings
from surveyor_backend.core.security import create_access_token
from surveyor_backend.schemas.user import UserLogin, UserOut
from surveyor_backend.schemas.token import Token
from surveyor_backend.services import auth_service

router = APIRouter()

@router.post("/login", response_model=Token)
def login(login_data: UserLogin):
    """
    Authenticate user and return access token + user info.
    """
    user = auth_service.authenticate_user(login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["id"])}, expires_delta=access_token_expires
    )
    
    # Returning BOTH the token and the user data as requested
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"],
            "is_active": user["is_active"]
        }
    }
