from fastapi import APIRouter
from api.v1.endpoints import auth
from api.v1.endpoints import gforms # Import your new file


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(gforms.router, prefix="/gforms", tags=["google-forms"])
