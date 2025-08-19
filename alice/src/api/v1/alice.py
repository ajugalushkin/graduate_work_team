import logging

from fastapi import APIRouter, Request

from schemas.alice import AliceResponse, AliceRequest, Response, ApplicationState

from schemas.enums import AliceRequestType, AliceCommandKeyword

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/webhook", summary="Alice webhook", response_model=AliceResponse)
async def webhook(request: Request):
    try:
        body = await request.json()
        logger.info("Raw request received: %s", body)

        alice_request = AliceRequest(**body)
        req_type = alice_request.request.type
        command = alice_request.request.command.lower()

        if req_type == AliceRequestType.WHAT_CAN_YOU_DO or req_type == AliceRequestType.HELP:
            return AliceResponse(
                response=Response(
                    text="Я умею искать режиссёра фильма. Спросите «Кто режиссёр фильма Star wars»",
                    tts="Я умею искать режиссёра фильма. Спросите «Кто режиссёр фильма Star wars»",
                    end_session=False,
                ),
                application_state=ApplicationState(value=37),
            )
        elif AliceCommandKeyword.START_SKILL.value in command:
            return AliceResponse(
                response=Response(
                    text="Здравствуйте! Я умею искать режиссёра фильма. Спросите: «Кто режиссёр фильма Star wars?»",
                    tts="Здравствуйте! Я умею искать режиссёра фильма. Спросите: «Кто режиссёр фильма Star wars?»",
                    end_session=True,
                ),
                application_state=ApplicationState(value=37),
            )
        else:
            return AliceResponse(
                response=Response(
                    text="Здравствуйте! Это мы, хороводоведы.",
                    tts="Здравствуйте! Это мы, хороводоведы.",
                    end_session=True,
                ),
                application_state=ApplicationState(value=37),
        )
    except Exception as e:
        logger.error("Error processing request: %s", e, exc_info=True)
        return AliceResponse(
            response=Response(
                text="Произошла ошибка. Попробуйте позже.",
                end_session=True,
            ),
            application_state=ApplicationState(value=37),
        )