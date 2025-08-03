import logging

from fastapi import APIRouter, Request

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/webhook", summary="Alice webhook", response_model=None)
async def webhook(request: Request):
    logger.info(request)
    logger.info(request.json())
