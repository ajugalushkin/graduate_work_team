import logging

from fastapi import APIRouter, Request

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/webhook", summary="Alice webhook", response_model=dict)
async def webhook(request: Request):
    logger.info(request)
    logger.info(await request.json())
    request = await request.json()
    if request["request"]["type"] == "Что ты умеешь":
        return {
            "response": {
                "text": "Я умею искать режиссёра фильма. Спросите «Кто режиссёр фильма Star wars»",
                "tts": "Я умею искать режиссёра фильма. Спросите «Кто режиссёр фильма Star wars»",
                "end_session": False
            },
            "application_state": {
                "value": 37
            },
            "version": "1.0"
        }
    elif "Запусти навык «кто режиссёр фильма»" in request["request"]["type"].lower():
        return {
            "response": {
                "text": "Здравствуйте! Я умею искать режиссёра фильма. Спросите: «Кто режиссёр фильма Star wars?»",
                "tts": "Здравствуйте! Я умею искать режиссёра фильма. Спросите: «Кто режиссёр фильма Star wars?»",
                "end_session": True
            },
            "application_state": {
                "value": 37
            },
            "version": "1.0"
        }
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