"""API package"""
from fastapi import APIRouter

from app.api import scans, tasks


router = APIRouter()

# Include sub-routers
router.include_router(scans.router, prefix="/scans", tags=["scans"])
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
