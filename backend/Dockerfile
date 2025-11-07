# Placeholder for Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
from pydantic import BaseModel, Field
from typing import List, Literal

class ClientAudio(BaseModel):
    chunk: bytes
    encoding: Literal["pcm_s16le"] = "pcm_s16le"
    sr: int = 16000

class STTPartial(BaseModel):
    text: str
    is_final: bool = False
    start_ms: int
    end_ms: int

class STTFinal(BaseModel):
    text: str
    is_final: bool = True
    start_ms: int
    end_ms: int

class ManagerRoute(BaseModel):
    intent: str
    agents: List[str]

class AgentRequest(BaseModel):
    agent: str
    text: str
    context: dict = Field(default_factory=dict)

class AgentUpdate(BaseModel):
    agent: str
    text: str

class AgentResult(BaseModel):
    agent: str
    result: dict
    confidence: float

class ManagerAnswer(BaseModel):
    text: str
    trace_id: str

class TTSAudio(BaseModel):
    chunk: bytes
    mime: Literal["audio/mpeg"] = "audio/mpeg"

class Error(BaseModel):
    code: int
    message: str

