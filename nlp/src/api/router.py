from fastapi import APIRouter

from src.api.v1 import health_router, movie_router

router = APIRouter()

router.include_router(health_router, prefix='/health', tags=['Health'])
router.include_router(movie_router, prefix="/movies", tags=["Movies"])