import logging

from fastapi import APIRouter, Request

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/webhook", summary="Alice webhook", response_model=dict)
async def webhook(request: Request):
    logger.info(request)
    logger.info(request.json())
    return {
        "response": {
            "text": "Здравствуйте! Это мы, хороводоведы.",
            "tts": "Здравствуйте! Это мы, хороводоведы.",
            "end_session": True
        },
        "application_state": {
          "value": 37
        },
        "version": "1.0"
    }