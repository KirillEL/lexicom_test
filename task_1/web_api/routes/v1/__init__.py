from fastapi import APIRouter
from .public import router as public_router

main_router = APIRouter()
main_router.include_router(public_router, dependencies=None)

__all__ = ['main_router']
