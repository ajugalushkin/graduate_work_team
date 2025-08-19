from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


# Request Models
class Meta(BaseModel):
    locale: str
    timezone: str
    client_id: str
    interface: Optional[Dict[str, Any]] = None


class RequestData(BaseModel):
    command: str
    original_utterance: str
    type: str
    markup: Optional[Dict[str, Any]] = None
    payload: Optional[Dict[str, Any]] = None


class Session(BaseModel):
    new: bool
    session_id: str
    user_id: str
    application: Dict[str, str]


class AliceRequest(BaseModel):
    meta: Meta
    request: RequestData
    session: Session
    version: str


# Response Models
class Response(BaseModel):
    text: str
    tts: Optional[str] = None
    end_session: bool = False


class ApplicationState(BaseModel):
    value: int


class AliceResponse(BaseModel):
    response: Response
    session_state: Optional[Dict[str, Any]] = None
    application_state: Optional[ApplicationState] = None
    version: str = "1.0"