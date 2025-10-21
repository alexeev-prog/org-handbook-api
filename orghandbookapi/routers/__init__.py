from .v1 import api_v1_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api")

api_router.include_router(api_v1_router)

all = ["api_router"]
