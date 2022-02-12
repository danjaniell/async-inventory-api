from app.api.endpoints import items
from fastapi import APIRouter

router = APIRouter()

router.include_router(items.router, tags=["items"], prefix="/items")
