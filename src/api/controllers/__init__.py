from fastapi import APIRouter

from .v1 import rag

routers_v1 = APIRouter(prefix="/api/v1")
routers_v1.include_router(rag.router, tags=["RAG: Обслуживание"])


__all__ = ["routers_v1"]
