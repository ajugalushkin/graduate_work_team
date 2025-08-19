from enum import StrEnum


class AliceRequestType(StrEnum):
    HELP = "Помощь"
    WHAT_CAN_YOU_DO = "Что ты умеешь"
    SIMPLE_UTTERANCE = "SimpleUtterance"
    BUTTON_PRESSED = "ButtonPressed"


class AliceCommandKeyword(StrEnum):
    START_SKILL = "запусти навык «кто режиссёр фильма»"