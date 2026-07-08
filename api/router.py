from fastapi import APIRouter

from api.chat import router as chat_router

#负责聚合所有 API
router = APIRouter()
router.include_router(chat_router)