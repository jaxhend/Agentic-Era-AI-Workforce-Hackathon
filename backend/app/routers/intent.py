from fastapi import APIRouter
from backend.app.schemas.schemas import TextIn, IntentOut
from ..agents import intent as agent

router = APIRouter(prefix="/intent", tags=["intent"])

@router.post("/analyze", response_model=IntentOut)
async def analyze(body: TextIn):
    intent = await agent.analyze(body.text)
    return IntentOut(intent=intent, confidence=0.75)

