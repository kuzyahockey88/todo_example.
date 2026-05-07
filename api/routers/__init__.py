from fastapi import APIRouter
from .task import router as task_router
from .category import router as category_router

api_router = APIRouter()
api_router.include_router(task_router, tags=["tasks"])
api_router.include_router(category_router, tags=["categories"])