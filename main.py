from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.api import api_router
from core.config import settings
from api.v1.endpoints import gforms # Import your new file

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
api_router.include_router(gforms.router, prefix="/gforms", tags=["google-forms"])

@app.get("/")
def root():
    return {"message": "Welcome to Surveyor Backend API", "docs": "/docs"}
