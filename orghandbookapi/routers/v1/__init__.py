from fastapi import APIRouter

from .activity import activity_router
from .building import building_router
from .organization import organizations_router

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(organizations_router, prefix="/organizations")
api_v1_router.include_router(activity_router, prefix="/activity")
api_v1_router.include_router(building_router, prefix="/building")

all = ["api_v1_router"]
