from fastapi import APIRouter

from .v1.alice import router as v1_alice_router

router = APIRouter()

router.include_router(v1_alice_router, tags=["Alice"], prefix="/v1/alice")
